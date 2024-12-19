import * as dotenv from 'dotenv';
import { Telegraf } from 'telegraf';
import axios from 'axios';

// Load environment variables from .env file
dotenv.config();

// Initialize the bot with your Telegram bot token
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN || '';
const GITHUB_TOKEN = process.env.GITHUB_TOKEN || '';
const GITHUB_USERNAME = process.env.GITHUB_USERNAME || '';
const REPOSITORY_NAME = process.env.REPOSITORY_NAME || '';

if (!TELEGRAM_BOT_TOKEN) throw new Error('Missing TELEGRAM_BOT_TOKEN');
if (!GITHUB_TOKEN) throw new Error('Missing GITHUB_TOKEN');
if (!GITHUB_USERNAME) throw new Error('Missing GITHUB_USERNAME');
if (!REPOSITORY_NAME) throw new Error('Missing REPOSITORY_NAME');

const bot = new Telegraf(TELEGRAM_BOT_TOKEN);

bot.start((ctx) => {
  ctx.reply('Welcome! Use /help to see available commands.');
});

bot.help((ctx) => {
  ctx.reply('Available commands:\n/create_gist - Create a new GitHub Gist');
});

bot.command('create_gist', async (ctx) => {
  try {
    const chatId = ctx.chat?.id;
    if (!chatId) throw new Error('Chat ID not found.');
    
    const markup = {
      reply_markup: {
        inline_keyboard: [
          [
            { text: 'Create Gist', callback_data: 'create_gist' }
          ]
        ]
      }
    };
    
    await ctx.reply('Click the button below to create a new Gist.', markup);
  } catch (error) {
    console.error('Error in /create_gist command:', error);
    ctx.reply('An error occurred while processing your request.');
  }
});

bot.on('callback_query', async (ctx) => {
  try {
    const callbackData = ctx.callbackQuery?.data;
    if (!callbackData) return;

    if (callbackData === 'create_gist') {
      const gistData = {
        description: 'Sample Gist created via Telegram bot',
        public: true,
        files: {
          'example.txt': {
            content: 'Hello, this is a sample Gist file!'
          }
        }
      };

      const response = await axios.post('https://api.github.com/gists', gistData, {
        headers: {
          'Authorization': `Bearer ${GITHUB_TOKEN}`,
          'Accept': 'application/vnd.github.v3+json'
        }
      });

      const gistUrl = response.data.html_url;
      ctx.reply(`Gist created successfully! You can view it here: ${gistUrl}`);
    }
  } catch (error) {
    console.error('Error handling callback query:', error);
    ctx.reply('An error occurred while processing your request.');
  }
});

bot.launch().then(() => {
  console.log('Bot is running...');
});

// Enable graceful stop for the bot
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
