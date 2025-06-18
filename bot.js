// bot.js
// Mineflayer bot that connects to a Minecraft server and listens for
// JavaScript commands over a WebSocket connection.

const mineflayer = require('mineflayer');
const WebSocket = require('ws');
require('dotenv').config();

// Create the Mineflayer bot using environment variables for config.
const bot = mineflayer.createBot({
  host: process.env.MC_HOST || 'localhost', // Minecraft server IP
  port: Number(process.env.MC_PORT) || 25565, // Minecraft server port
  username: process.env.MC_USERNAME || 'ChatGPTBot', // Bot username
  password: process.env.MC_PASSWORD // Optional, for online-mode servers
});

bot.on('spawn', () => console.log('Bot spawned and ready.'));
bot.on('error', err => console.error('Bot error:', err));
bot.on('end', () => console.log('Bot disconnected.'));

// Create a WebSocket server to receive commands from the Python script.
const wss = new WebSocket.Server({ port: Number(process.env.BOT_PORT) || 3001 });
console.log(`WebSocket server listening on port ${process.env.BOT_PORT || 3001}`);

wss.on('connection', ws => {
  ws.on('message', message => {
    console.log('Received command:', message.toString());
    try {
      // Wrap the received JavaScript code in a function and execute it.
      // This allows GPT to send code like: "bot.chat('Hello world')".
      const fn = new Function('bot', message.toString());
      fn(bot);
      ws.send('Command executed.');
    } catch (err) {
      console.error('Failed to execute command:', err);
      ws.send('Error: ' + err.message);
    }
  });

  ws.send('Connected to Minecraft bot.');
});
