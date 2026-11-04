import express from "express";
import { z } from "zod";
import { pickLang } from "./i18n.js";
import { SHOP_EMAIL, type Mailer } from "./mailer.js";
import { renderHome } from "./render.js";

const ContactForm = z.object({
  name: z.string().trim().min(1).max(100),
  email: z.string().trim().email().max(200),
  message: z.string().trim().min(1).max(2000),
});

export interface AppDeps {
  mailer: Mailer;
}

export function createApp({ mailer }: AppDeps) {
  const app = express();
  app.use(express.urlencoded({ extended: false, limit: "20kb" }));
  app.use(express.static("public"));

  app.get("/", (req, res) => {
    const lang = pickLang(req.query.lang);
    res.type("html").send(renderHome(lang, { sent: req.query.sent === "1" }));
  });

  app.post("/contact", async (req, res, next) => {
    const lang = pickLang(req.query.lang);
    const parsed = ContactForm.safeParse(req.body);
    if (!parsed.success) {
      res.status(400).type("html").send(renderHome(lang, { error: true, values: req.body }));
      return;
    }
    try {
      const { name, email, message } = parsed.data;
      await mailer.send({ to: SHOP_EMAIL, replyTo: email, subject: `Web: správa od ${name}`, text: message });
      res.redirect(303, `/?lang=${lang}&sent=1#contact`);
    } catch (err) {
      next(err);
    }
  });

  return app;
}
