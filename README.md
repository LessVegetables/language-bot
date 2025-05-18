# ChatTutor

ChatTutor is Telegram chatbot designed to complement language learning by providing realistic conversation practice. It is designed to supplement traditional language learning by offering users a realistic conversation partner—helping them build practical language skills through natural dialogue.


## Overview

- **Purpose**: ChatTutor offers users the opportunity to practice a language in a conversational setting. The bot simulates real-life interactions, encouraging users to communicate in the language they are learning. It is intended as a supportive tool in the broader language learning process, complementing the role of human tutors rather than replacing them.

- **Current Features**: 
  - **Text-Only Interaction**: For now, the bot supports unlimited text messaging with one "character" acting as your tutor.
  - **Natural Conversations**: The bot responds naturally, keeping the flow of conversation engaging and lifelike. It can explain concepts if asked, but its main role is to act as a conversation partner.

  
## Planned Enhancements

The project roadmap includes several exciting features aimed at enriching the learning experience and expanding functionality:

- **Multiple Tutor Personalities**: Allowing users to choose from various tutor characters with different personality traits.

- **Media Integration**: Adding support for sticker recognition, voice messages, and potentially video messages.

- **Tutoring Plans**: Future monetization strategies may offer tutoring plans where educators can invest in bulk usage, providing their students with free access to ChatTutor’s features while keeping core interactions accessible to all users.

- **Monetization Model**: Although messaging is currently unlimited, a future monetization strategy will introduce rate limits. Early adopters will retain unlimited text messaging and receive limited free access to premium features (like voice messages) as a token of appreciation.

## Technical Details

- **Language & Frameworks**: 
  - **Python**: The project is built using Python, leveraging its robust ecosystem for asynchronous programming.
  - **Asynchronous Operations**: All interactions and database operations run asynchronously for efficient performance.
- **Database**: 
  - **PostgreSQL**: Utilized for managing user data, conversation logs, and configuration settings.
- **Localization**:
  - **gettext**: Implemented for language localization in the settings menu and onboarding process, ensuring a smooth user experience across multiple languages.

## Installation & Setup

If you’d like to run or contribute to ChatTutor locally, follow these steps:


1. **Clone the Repository**:

   ```bash
   git clone https://github.com/LessVegetables/language-bot
   ```
2. **Navigate to the Project Directory**:

   ```bash
   cd language-bot
   ```
3. **Create virtual environment** (optional but recommended):

	```bash
	python -m venv venv
	```
4. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
5. **Configure Environment Variables**:  
   Create a `.env` file with the following:

   ```env
   BOT_TOKEN=<your-telegram-bot-token>
   OPENAI_API_KEY=<your-open-ai-key>
   
   POSTGRES_USER=<your-postgresql-username>
   POSTGRES_PASSWORD=<your-postgresql-password>
   POSTGRES_DB=<your-postgresql-database-name>
   ```
6. **Run the Bot**:

   ```bash
   python src/mvp.py
   ```

## Collaborators

ChatTutor represents a forward-thinking project that leverages natural language processing, asynchronous programming in Python, and robust database management to create a dynamic language learning tool. Key highlights include:

- **Scalable Architecture**: Efficiently handles high concurrency and user growth through asynchronous operations and PostgreSQL.
- **User-Centric Design**: Focused on enhancing the language learning process by providing a realistic, engaging conversation experience—not as a replacement for human tutors, but as a valuable supplement.
- **Internationalization**: Built with localization in mind, ensuring accessibility and usability for a global audience.
- **Future-Proofing**: With a clear roadmap that includes multi-character support, media enhancements, and tutoring plans, ChatTutor is poised to evolve with the needs of modern language learners.

## Contributing

Contributions are welcome! If you'd like to improve ChatTutor, please fork the repository, make your changes, and open a pull request. For major changes, please open an issue first to discuss your ideas.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.