export interface Mail {
  to: string;
  replyTo?: string;
  subject: string;
  text: string;
}

export interface Mailer {
  send(mail: Mail): Promise<void>;
}

/** Development mailer: prints instead of sending. Production wires an SMTP mailer here. */
export class ConsoleMailer implements Mailer {
  async send(mail: Mail): Promise<void> {
    console.log(`[mail] to=${mail.to} subject=${mail.subject}\n${mail.text}`);
  }
}

export const SHOP_EMAIL = process.env.SHOP_EMAIL ?? "objednavky@kvasok.example";
