import { createApp } from "./app.js";
import { ConsoleMailer } from "./mailer.js";

const port = Number(process.env.PORT ?? 3000);
createApp({ mailer: new ConsoleMailer() }).listen(port, () => {
  console.log(`Kvások & syn on http://localhost:${port}`);
});
