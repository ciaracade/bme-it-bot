# Biomedical Engineering IT Dept Slack Bot
👩🏽‍💻 A chatbot that seamlessly integrates **TeamDynamix**, **OpenAI**, and **Slack** to streamline ticket management for the **University of Michigan Biomedical Engineering IT Department**. 

---

## 🚀 Features
- **TeamDynamix Integration**: Automatically fetch, create, and update tickets directly from Slack.
- **OpenAI-Powered Assistance**: Smart suggestions and automated responses to common IT queries.
- **Slack Workflow Compatibility**: Seamless integration with existing Slack channels and workflows.
- **Time-Saving**: Reduces manual effort, allowing IT staff to focus on more critical tasks.

---

## 📖 Table of Contents
1. [Getting Started](#getting-started)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Configuration](#configuration)
5. [Features in Depth](#features-in-depth)
6. [Contributing](#contributing)
7. [License](#license)
8. [Contact](#contact)

---

## 🛠️ Getting Started
### Prerequisites
- Node.js (v14+ recommended)
- Slack Workspace with bot permissions
- TeamDynamix API credentials
- OpenAI API key

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/bme-it-slackbot.git
   cd bme-it-slackbot
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Configure the environment variables (see [Configuration](#configuration)).

---

## ⚙️ Configuration
Create a `.env` file in the root directory with the following variables:
```env
SLACK_BOT_TOKEN=your-slack-bot-token
TEAMDYNAMIX_API_KEY=your-teamdynamix-api-key
OPENAI_API_KEY=your-openai-api-key
```

---

## 💻 Usage
Start the bot with:
```bash
npm start
```
Once running, invite the bot to your desired Slack channel and start interacting with it using commands like `/ticket create` or `/help`.

---

## 📚 Features in Depth
- **Ticket Creation**: Use `/ticket create` to generate a new ticket in TeamDynamix.
- **Status Updates**: Query ticket statuses with `/ticket status <ticket_id>`.
- **AI Responses**: Get natural language answers to technical queries using OpenAI's API.
- **Custom Commands**: Easily add custom commands for your department's unique workflows.

---

## 🤝 Contributing
We welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes and push:
   ```bash
   git commit -m "Add your feature description"
   git push origin feature/your-feature
   ```
4. Open a Pull Request.

---

## 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 📬 Contact
For questions or support, please reach out to the **Biomedical Engineering IT Department** at `it-support@umich.edu`.

### Key Enhancements:
- **Professional structure**: Well-defined sections make it easy for users to navigate.
- **Concise explanations**: Avoids unnecessary complexity while remaining informative.
- **Focus on University branding**: Reflects a professional academic setting.
- **Actionable steps**: Simplifies setup for new users or contributors.

Let me know if you'd like to refine this further!