commands_eng = {
    '/start': "👋 Welcome to Tomas Karlows's private community.\n"
              "Chose one of the avaikable features:\n"
              "- Risk calculator\n"
              "- Trading strategy selections",
    '/trade_volume': '🔢 Trading Calculator. Calculates the required position size for trading on cryptocurrency '
                     'exchanges. 💹',
    '/help_me_eng': "Hello! I am a bot that provides a trading calculator function.\n\n"
             "To use the calculator, select the language using the command:\n"
"/trade_volume_RU - for Russian\n"
"/trade_volume_ENG - for English\n\n"
"Follow the instructions to enter the necessary parameters and calculate the position volume.",

    '/cancel_none': 'There is nothing to cancel or interrupt at the moment.\n\n'
                    'Use the /start command to choose an action.',
    '/cancel': 'You have exited data entry.\n\n'
               'Use the /start command to choose an action.',
    'trade_start_eng': '💰 Enter the coin you are interested in.\n\n'
                   'Input format: capital letters in Latin.\n'
                   'Example: BTCUSDT, ETHUSDT, XRPUSDT, NEARUSDT 📈',
    'currency': '📝 Please enter a decimal number for the entry price into the position 💹\n\n'
                '❓ It is important to consider that the entry price affects your potential profit and risk. '
                'Try analyzing charts and support/resistance levels to determine the best entry price.',
    'bad_currency': '❌ The entered value is not correct.\n\n'
                    '📋 Example: BTCUSDT, ETHUSDT, NEARUSDT\n'
                    '🔡 The currency pair is specified in capital Latin letters, without spaces!\n\n'
                    '🚫 If you changed your mind, use the /cancel command.',

    'entry_price_2': '📝 Please enter a decimal number for the exit price out of the position 💹\n\n'
                     '❓ The exit price out of the position (stop-loss) determines your potential loss '
                     'if the trade ends unsuccessfully. When analyzing the exit price, consider support/resistance '
                     'levels '
                     'and your risk management strategy.',
    'bad_entry': '❌ The entered value is not a number.\n\n'
                 '🚫 If you changed your mind, enter /cancel.',

    'stop_loss_2': '💹 Specify the leverage size from 1 to 120 💹\n\n'
                   '❓ Leverage determines the scale of your trading. '
                   'The higher the leverage, the greater the potential profit (and loss), '
                   'but also the higher the risk. Analyze your capabilities and risks carefully '
                   'when choosing the leverage level.',
    'bad_stop_loss': '❌ The entered value is not a number or a floating point number.\n\n'
                     '🚫 If you changed your mind, enter /cancel',
    'leverage_2': '💰 Please enter the deposit amount as an integer 💰\n\n'
                  '❓ The deposit amount affects your trading strategy and risk level. '
                  'This is an important parameter that should be carefully considered '
                  'when making trading decisions. '
                  'Make sure that your risk matches your financial capabilities and trading strategy.',
    'bad_leverage': '❌ The entered value is not a number or does not fall within the range from 1 to 120.\n\n'
                     '🚫 If you changed your mind, enter /cancel',
    'deposit_2': '📈 Please enter the risk percentage from 1 to 100 📈\n\n'
                 '❓ The risk percentage determines how much of your deposit you are willing to lose in one trade. '
                 'This is a key parameter for managing your investments and controlling losses. '
                 'Choose a risk percentage that matches your comfort level and trading strategy.',
    'bad_deposit': '❌ The entered value is not a number.\n\n'
                     '🚫 If you changed your mind, enter /cancel',
    'percent_2': '💰 Please enter the exchange commission rate as a floating-point number 💰\n\n'
                  '❓ Exchange commission is additional costs charged by the exchange for each trade. '
                  'It affects the total costs of your trading and should be taken into account when calculating your '
                 'risk and profit. '
                  'Examples of exchange commissions:\n'
                  ' - Bybit: 0.075% (maker), 0.15% (taker)\n'
                  ' - OKX: 0.1% (maker), 0.15% (taker)\n'
                  ' - Binance: 0.1% (maker), 0.1% (taker)\n\n'
                  'Choose a commission that matches your broker or exchange where you trade.',
    'bad_percent': '❌ The entered value is not a number or does not fall within the range from 1',
    'signal_1': "Welcome to Tomas Kralow's private community, this versatile bot assistant will"
             "work with parameters set by you and provide individual assistance in trading.\n\n"
             "To work effectively, choose a trading strategy based on your risk preferences.\n"
             "There are 3 strategies available:\n\n"
                "1⃣ Gold Standard\n"
             "This is the most balanced strategy of all. You will receive confident signals with"
             "moderate risks, your deposit will always be safe, "
             "and you will consistently show average profit performance.\n\n"
                "2⃣ High Risk\n"
             "this strategy is suitable for those willing to take high risk."
             "Higher risks bring higher potential returns, but keep in mind that the "
             "probability of sharp draw downs also exists.\n\n"
                "3⃣ This strategy is suitable for those not willing to take high risk and"
             "want their funds to be safe, while also having a relatively smooth deposit"
             "performance. By choosing this strategy, you will mostly work on the spot and "
             "assembly a medium-term portfolio that will perform well in a bull market.\n\n",
    # 'gold_standard': "1⃣ Gold Standard\n"
    #          "This is the most balanced strategy of all. You will receive confident signals with"
    #          "moderate risks, your deposit will always be safe, "
    #          "and you will consistently show average profit performance.\n\n",
    # 'high_risk': "2⃣ High Risk\n"
    #          "this strategy is suitable for those willing to take high risk."
    #          "Higher risks bring higher potential returns, but keep in mind that the "
    #          "probability of sharp draw downs also exists.\n\n",
    # 'passive_portfolio': "3⃣ Passive Portfolio\n"
    #          "This strategy is suitable for those not willing to take high risk and"
    #          "want their funds to be safe, while also having a relatively smooth deposit"
    #          "performance. By choosing this strategy, you will mostly work on the spot and "
    #          "assembly a medium-term portfolio that will perform well in a bull market.\n\n",
    'gold_choose': '🏆 You have chosen the gold standard strategy.\n\n'
                   'Moving forward, the bot will automatically send you signals and calculate the '
                   'position size you should enter. 📊\n\n'
                   'Please enter the size of your deposit so that the bot can accurately calculate the risks. 💰\n\n',
    'high_risk_choose': '🚨 You have chosen the High Risk strategy.\n\n'
                        'Please be aware that changes in deposit size can occur '
                        'very rapidly in this strategy. Please closely monitor risk management. 👀\n\n'
                        'In the future, the bot will automatically send you signals and calculate the '
                        'appropriate position size for you to enter. 📊\n\n',
    'passive_choose': '🌱 You have chosen the passive portfolio strategy.\n\n'
                      'Moving forward, the bot will automatically send you signals and calculate the'
                      ' position size you should enter. 📊\n\n'
                      'Please enter the size of your deposit so that the bot can accurately calculate the risks. 💰\n\n',
    'after_input_deposite': 'Thank you. 👍\n\n'
       'If you want to change your trading strategy, you can do it through the bot`s menu, but we want to note that '
                            'it is not advisable to do it frequently, or your trading will not be stable. ⚠️\n\n '
       'In the future, all you need to do to work is enter the necessary values for limit orders on the exchange. 📊\n\n'
       'Stay tuned for signals! 📣'

}
