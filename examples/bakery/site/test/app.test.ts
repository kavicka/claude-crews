import request from "supertest";
import { describe, expect, it } from "vitest";
import { createApp } from "../src/app.js";
import type { Mail, Mailer } from "../src/mailer.js";

class FakeMailer implements Mailer {
  sent: Mail[] = [];
  async send(mail: Mail) {
    this.sent.push(mail);
  }
}

function setup() {
  const mailer = new FakeMailer();
  return { mailer, app: createApp({ mailer }) };
}

describe("home page", () => {
  it("renders Slovak by default with the menu and prices", async () => {
    const res = await request(setup().app).get("/");
    expect(res.status).toBe(200);
    expect(res.text).toContain('lang="sk"');
    expect(res.text).toContain("Kváskový chlieb 1 kg");
    expect(res.text).toMatch(/5,20\s€/);
  });

  it("renders English with ?lang=en", async () => {
    const res = await request(setup().app).get("/?lang=en");
    expect(res.text).toContain('lang="en"');
    expect(res.text).toContain("Sourdough loaf 1 kg");
  });

  it("shows Monday as closed", async () => {
    const res = await request(setup().app).get("/?lang=en");
    expect(res.text).toContain("Monday: closed");
  });
});

describe("contact form", () => {
  it("emails the shop and redirects with a confirmation", async () => {
    const { app, mailer } = setup();
    const res = await request(app)
      .post("/contact?lang=en")
      .type("form")
      .send({ name: "Eva", email: "eva@example.com", message: "Two loaves for Saturday?" });
    expect(res.status).toBe(303);
    expect(res.headers.location).toBe("/?lang=en&sent=1#contact");
    expect(mailer.sent).toHaveLength(1);
    expect(mailer.sent[0]).toMatchObject({ replyTo: "eva@example.com", text: "Two loaves for Saturday?" });
  });

  it("rejects an invalid email and keeps the typed values, escaped", async () => {
    const { app, mailer } = setup();
    const res = await request(app)
      .post("/contact")
      .type("form")
      .send({ name: "<b>Eva</b>", email: "nope", message: "Hi" });
    expect(res.status).toBe(400);
    expect(res.text).toContain("&lt;b&gt;Eva&lt;/b&gt;");
    expect(mailer.sent).toHaveLength(0);
  });
});
