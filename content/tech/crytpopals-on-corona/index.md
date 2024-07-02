+++
title = "Hacking block ciphers on 3 beers"
date = 2024-06-30 # 00:19 start
+++

It's summer. I'm bored out of my mind. A little depressed too, remind you I am
going through a breakup..  
There are 3 large (355ml) coronas in the fridge and I'm feeling intelectually
understimulated - work has been fine but I haven't had to write much code over
the past 1-2 weeks.

[cryptopals](https://cryptopals.com) is a cryptography CTF-style problem set
that I [started](https://github.com/mitiko/cryptopals/releases/tag/set1%2Fchallange1)
back in October last year, so I thought it's a perfect choice for a drunk night
~out~ in.  
Generally [coding under the influence](https://brej.org/edit/influence/) is not
a good idea but it has its advantages - it's harder to think of overly
complicated solutions so you tend to write more and smaller functions and your
code _can be_ more readable.

<!-- TODO: beer visual counter -->

It's already 0:45 and I've downed one beer, let's see how far along I can keep
it going before I get too sleepy.

First I reviewed the last challenge I did - it was challenge 17 from set 3 about
CBC decryption from a padding oracle. I went through the code and although
I don't get 100% of the logic right away, I've left plenty of comments to get
by.  
On to challange 18!

## Challenge 18

From the description:

> Implement CTR, the stream cipher mode.  
> Instead of encrypting the plaintext, CTR mode encrypts a running counter,
> producing a 16 byte block of keystream, which is XOR'd against the plaintext.  
> Decrypt the string at the top, then use your CTR function to encrypt and
> decrypt other things.

Okay, seems like we're just adding new functionality here, nothing too shady.  
The [wiki page](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Counter_(CTR))
on it is pretty good too:

![diagram of CTR and other AES encryption modes](aes.png)

I'll just use my `aes128_ecb_encrypt` function to write something stateless
where it encrypts plaintext given a counter and a key (and a nonce).

```rust
fn aes128_ctr_iteration(plaintext_block: &[u8; 16], nonce: u64, counter: u64) -> Vec<u8> {
    todo!()
}
```

So far I've put my ECB and CBC implementations in separate modules, so I'll do
the same for CTR.
The implementation is pretty straight-forward - we create an ECB-style key by
concatenating the nonce and counter (with a bit shift), then the tricky part is
to use little endian for each of the nonce and counter but concatenate them
BE-style.

```rust
pub fn aes128_ctr_iteration(plaintext_block: &[u8], key: &[u8; 16], nonce: u64, counter: u64) -> Vec<u8> {
    assert!(plaintext_block.len() <= 16);
    let iv_cntr_pair = [nonce.to_le_bytes(), counter.to_le_bytes()].concat();
    let iteration_block = aes128_ecb_encrypt(key, &iv_cntr_pair);
    xor(&iteration_block, plaintext_block)
}
```

Whereas this would be incorrect:

```rust
let iv_cntr_pair = (u128::from(nonce) << 64 | u128::from(counter)).to_le_bytes();
```

Being a little too clever (which I might do if I wasn't halfway through my
second beer):

```rust
let iv_cntr_pair = (u128::from(counter) << 64 | u128::from(nonce)).to_le_bytes();
```

Technically I'm cheating a bit when generating the extpected test output but
seasoned TDD devs will call this [snapshot testing](https://en.wikipedia.org/wiki/Software_testing#Output_comparison_testing).

```rust
#[test]
fn aes128_ctr_single_iteration() {
    let key = b"YELLOW SUBMARINE";
    let (nonce, counter) = (3 << 32, 1);
    let data = b"Lorem ipsum dolo";
    let ciphertext = aes128_ctr_iteration(data, nonce, counter);
    assert_eq!(String::from_utf8_lossy(&raw_to_hex(&ciphertext)), "");
    assert_eq!(raw_to_hex(&ciphertext), b"what do i put here?");
}
```

Then I just copy the structure of my CBC code to iterate over the blocks
incrementing the counter and we're done.

```rust
pub fn aes128_ctr_iteration(plaintext_block: &[u8], key: &[u8; 16], nonce: u64, counter: u64) -> Vec<u8> {
    assert!(plaintext_block.len() <= 16);
    let iv_cntr_pair = (u128::from(counter) << 64 | u128::from(nonce)).to_le_bytes();
    let iteration_block = aes128_ecb_encrypt(key, &iv_cntr_pair);
    xor(&iteration_block, plaintext_block)
}
```

Finished my second beer now. I'm putting a frozen pizza in the oven and cracking
the third. It's really a 10-minute timer battle against my food to solve the
challenge. To be frank, the alcohol is making me a bit cloudy, I initially used
the nonce + counter as the key, which is wrong but thankfully I caught this by
testing decryption is symmetric.

Okay, maybe I underestimated the task but only because some of the set1/set2
challenges were implementation only.
> decrypts to something approximating English in CTR mode

This info is more relevant now.

Since we know the initial nonce and counter, we know the plaintext from ECB's
perspective for each block:

```
ciphertext[..16] = ECB(key, [nonce, counter]) ^ plaintext[..16]
plaintext[..16] = ciphertext[..16] ^ ECB(key, [nonce, counter])
plaintext[16..32] = ciphertext[16..32] ^ ECB(key, [nonce, counter + 1])
plaintext[32..48] = ciphertext[32..48] ^ ECB(key, [nonce, counter + 2])
```

We can ignore the nonce/counter and treat `ECB(..)` as random, then use our XOR
English frequency attack to guess the result. Except due to the counter change
at each block the "key" is not repeated, and we can't use the hamming distance
trick. Hmm..

Oh.. okay, we have the key too, doing the statistical attack is part of
challange 20. So it is just implementation only after all!

## Challenge 19

It's 03:57 now and I'm out of beers, might have to hit the skateboard and check
the 24x7 store out for more. 19 and 20 seem pretty easy tho, so I'll go after.

```rust
#[test]
fn challange19() {
    let plaintexts = read_base64_lines("data/set3/challenge19.txt");
    let key = rand::rngs::StdRng::from_seed([57; 32]).gen();
    let ciphertexts: Vec<_> = plaintexts
        .iter()
        .map(|p| aes128_ctr_encrypt(&p, &key, 0, 0))
        .collect();

    drop(key); // hehe
    let mut decoded = vec![Vec::new(); ciphertexts.len()];

    // TODO: crack cipher
    assert!(String::from_utf8_lossy(&decoded[5]).contains("polite meaningless words")); // peeked in plaintexts
    assert!(String::from_utf8_lossy(&decoded[34]).contains("yet I number him in the song"));
}
```

Rust is cool in that I can ensure the key never gets used anymore. Also that
line of code is pretty funny. I wonder if I've done this elsewhere in this
codebase..

Now I just make my `xor_cross_entropy_analysis` from set 1 public and transpose
the ciphertexts. The challenge specifies for a tad bit more but I feel like this
satisfies the criteria, they do ask to "not overthink it" after all.  
Of course, the last few bytes (columns) of all ciphertexts are a tiny sample size and
won't produce any statistically relevant information, so we're effectively only
breaking prefixes. With a big enough dictionary all guesses are verifiable
though.

## Challenge 20

Pretty much the same thing but concatenate it in one big string first:

```rust
let len = ciphertexts.iter().map(|c| c.len()).min().unwrap();
let mut long_cipher: Vec<u8> = Vec::with_capacity(len * ciphertexts.len());
for ciphertext in ciphertexts {
    long_cipher.extend(&ciphertext[..len]);
}
```

Then a little refactoring to expose the solution function from set 1, and it's
done. Variable naming questionable ofc :))

```rust
let key = break_rep_xor(&long_cipher);
let long_plain = xor_rep(&long_cipher, &key);
let decoded: Vec<_> = long_plain.chunks_exact(len).map(|x| x.to_vec()).collect();
```

## Skateboard

It's 5am now, I had one energy drink + the pizza + XOR-ing are sobering me up.

## Challenge 21

> Implement the MT19937 Mersenne Twister RNG  
> You can get the psuedocode for this from Wikipedia.

Finally something fun!

From wikipedia:

>



