const app = require('./app');
const { syncDatabase } = require('./models');

const PORT = process.env.PORT || 8004;

const start = async () => {
    await syncDatabase();
    app.listen(PORT, () => {
        console.log(`ms-matching corriendo en http://localhost:${PORT}`);
    });
};

start();