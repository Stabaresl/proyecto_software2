const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransport({
    host:   process.env.EMAIL_HOST,
    port:   parseInt(process.env.EMAIL_PORT),
    secure: false,
    auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASS,
    },
});

const enviarEmail = async ({ to, subject, html }) => {
    if (!process.env.EMAIL_USER || !process.env.EMAIL_PASS) {
        console.log(`[EMAIL SIMULADO] Para: ${to} | Asunto: ${subject}`);
        return;
    }

    await transporter.sendMail({
        from:    process.env.EMAIL_FROM,
        to,
        subject,
        html,
    });
};

module.exports = { enviarEmail };