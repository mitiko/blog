+++
title = "Rust"
date = 2024-06-27
aliases = ["/ref/rs"]
+++

### Error Handling

I've found the easiest way to do error handling with the most control is a
global error enum. This captures all dependency crate error types, as well as
any custom application error types.

```rust
#[derive(Debug)]
enum GlobalError {
    Tera(tera::Error),
    Notify(notify::Error),
    Sqlite(rusqlite::Error),
    Io(std::io::Error),
    App(app_error::AppError),
}
```

I'd also recommend implementing `From<T>` for all dependency error types,
so that `?` works flawlessly.

```rust
impl From<tera::Error> for GlobalError {
    fn from(err: tera::Error) -> Self {
        GlobalError::Tera(err)
    }
}

impl From<notify::Error> for GlobalError {
    fn from(err: notify::Error) -> Self {
        GlobalError::Notify(err)
    }
}
```

## Web

For web servers I'm most familiar with [axum][1], I think the ecosystem is pretty rad.

### Simple Web Server

Remember to implement `IntoResponse` for `GlobalError`!

```rust
#[tokio::main]
async fn main() -> Result<(), GlobalError> {
    use axum::routing::{get, post};
    use tower_http::services::ServeDir;

    let app = axum::Router::new()
        .route("/", get(http_get_data))
        .route("/", post(http_post_data))
        .nest_service("/static", ServeDir::new("static"))
        .fallback(http_not_found);

    let socket = tokio::net::TcpListener::bind("0.0.0.0:8080").await?;
    println!("Listening on http://{}", socket.local_addr()?);
    axum::serve(socket, app).await?;

    Ok(())
}

use axum::response::{Html, IntoResponse};
async fn http_get_data() -> Result<impl IntoResponse, GlobalError> {
    Ok(Html("<h1>Hello world!</h1>"))
}
```

### Tera Engine

I like the [Tera][2] engine, it's used by [Zola][3] and it's very similar to
Jinja.  
This is how you register Tera with [axum][1]:

```rust
use tokio::sync::Mutex;
use std::sync::Arc;
use tera::Tera;

#[tokio::main]
async fn main() -> Result<(), GlobalError> {
    let tera_engine = Tera::new("templates/**/*.html")?;
    let tera_mutex = Arc::new(Mutex::new(tera_engine));

    use axum::routing::{get, post};
    let app = axum::Router::new()
        .route("/", get(http_main))
        .layer(axum::Extension(tera_mutex.clone()));

    // tera_hot_reload(tera_mutex, "templates")?;

    let socket = tokio::net::TcpListener::bind("0.0.0.0:8080").await?;
    println!("Listening on http://{}", socket.local_addr()?);
    axum::serve(socket, app).await?;

    Ok(())
}

type TeraEngine = Extension<Arc<Mutex<tera::Tera>>>;

async fn http_main(Extension(tera): TeraEngine) -> Result<impl IntoResponse, GlobalError> {
    let mut context = tera::Context::new();
    context.insert("number", &5);

    Ok(tera.lock().await.render("main.html", &context).map(Html)?)
}
```

Perhaps you can use some serde magic to serialize structs into `tera::Context`.

### Tera Engine Hot Reload

When actively developing tera templates, it's beneficial to setup hot reload.
The standard Rust way is using [notify][4]. It has different watchers depending
on your OS. By default you setup `RecommendedWatcher` and it uses macros to best
choose for you.

```rust
fn tera_hot_reload(tera_mutex: Arc<Mutex<Tera>>, directory: &str) -> Result<(), GlobalError> {
    use notify::Watcher;

    let (file_change_tx, mut file_change_rx) = tokio::sync::mpsc::channel(16);

    let mut watcher = notify::RecommendedWatcher::new(
        move |_| file_change_tx.blocking_send(()).unwrap(),
        notify::Config::default(),
    )?;
    watcher.watch(
        std::path::Path::new(directory),
        notify::RecursiveMode::Recursive,
    )?;

    tokio::spawn(async move {
        while let Some(_) = file_change_rx.recv().await {
            // println!("[notify] reloading");
            if let Err(e) = tera_mutex.lock().await.full_reload() {
                eprintln!("[notify/tera] ERROR: {e:?}");
            }
        }
    });

    Ok(())
}
```


[1]: https://docs.rs/axum/latest/axum/
[2]: https://keats.github.io/tera/
[3]: https://www.getzola.org/documentation/getting-started/overview/
[4]: https://docs.rs/notify/latest/notify/
