# Minecraft GPT Bot

This project connects a Minecraft bot powered by [Mineflayer](https://github.com/PrismarineJS/mineflayer) to OpenAI's GPT-4.  
You can type natural language instructions like "go chop wood" and GPT-4 will translate them into JavaScript code the bot executes.

## Files

- **bot.js** – Node.js Mineflayer bot exposing a WebSocket server.
- **gpt_server.py** – Python script that sends your instructions to GPT-4 and forwards the generated code to the bot.
- **package.json** – Node dependencies (Mineflayer, ws, dotenv).
- **requirements.txt** – Python dependencies (openai, websockets, python-dotenv).
- **.env.example** – Example configuration file.
- **gui.py** – Optional Tkinter GUI to send commands without the terminal.

## Setup

1. **Clone the repository** and install Node & Python dependencies:

   ```bash
   npm install
   pip install -r requirements.txt
   ```

2. **Create a `.env` file** based on `.env.example` and fill in your Minecraft server details and OpenAI API key.

3. **Start the bot**:

   ```bash
   node bot.js
   ```

4. **Run the GPT command server** (in another terminal):

   ```bash
   python gpt_server.py
   ```

   Type instructions after the `bot>` prompt. Example:

   ```
   bot> go chop wood
   ```

   GPT-4 might return code such as:

   ```javascript
   // Example response from GPT-4
   bot.chat('On my way to chop wood!');
   const tree = bot.findBlock({matching: block => block.name.includes('log')});
   if (tree) await bot.pathfinder.goto(new GoalBlock(tree.position.x, tree.position.y, tree.position.z));
   ```

   The Node bot receives this JavaScript and executes it.

5. **Use the optional GUI** (instead of the terminal):

   ```bash
   python gui.py
   ```

   Enter commands in the text box and press **Send**. You can create a Windows
   executable with [PyInstaller](https://pyinstaller.org/) after installing it:

   ```bash
   pip install pyinstaller
   pyinstaller --onefile --windowed gui.py
   ```

   The resulting `dist/gui.exe` launches the GUI without needing Python
   installed.

## Safety

Commands received over WebSocket are executed with `new Function`.  
Use this only in controlled environments and never expose the WebSocket port publicly.

## Notes

- Mineflayer provides many helpers for navigation, mining, building, etc.  Consult the documentation to craft more advanced instructions.
- The OpenAI API may return code that needs slight adjustments.  Review output in your terminal before running in production.

Enjoy experimenting with your GPT-powered Minecraft bot!
