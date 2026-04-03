require('dotenv').config();
const app       = require('./app');
const mongoose  = require('mongoose');

const PORT     = process.env.PORT || 8005;
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/tb_notificaciones';

const start = async () => {
    await mongoose.connect(MONGO_URI);
    console.log('MongoDB conectado — tb_notificaciones');
    app.listen(PORT, () => {
        console.log(`ms-notificaciones corriendo en http://localhost:${PORT}`);
    });
};

start();