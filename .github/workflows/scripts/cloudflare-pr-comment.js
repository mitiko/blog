// module.exports = ({github, context}) => {
//     return context.payload.client_payload.value
// }
module.exports = ({qrcode}) => {
    // return context.payload.client_payload.value
    const branch = "neg-13-deg"
    const url = `https://${branch}.mitiko.pages.dev/`;
    new qrcode({
        content: url,
        padding: 2,
        width: 192,
        height: 192,
        color: "#f48120",
        background: "#ffffff",
        ecl: "Q", // 25%
      });
      return `data:image/svg+xml;base64,${btoa(qrcode.svg())}`;
}