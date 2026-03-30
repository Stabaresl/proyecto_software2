const app       = require('./app');
const connectDB = require('./config/db');

const PORT = process.env.PORT || 8005;

const start = async () => {
    await connectDB();
    app.listen(PORT, () => {
        console.log(`ms-notificaciones corriendo en http://localhost:${PORT}`);
    });
};

start();