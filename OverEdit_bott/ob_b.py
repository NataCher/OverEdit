import telebot
from telebot import types
import sqlite3
from sqlite3 import Error

bot = telebot.TeleBot('6887025893:AAGwoLCvQDkV9xfcLm7Fej3TLbFDt_WF7Lc')

bot.videos = []
bot.current_video_index = 0
bot.current_theme = ""
bot.user_id = 0

def create_connection():
    try:
        conn = sqlite3.connect('over.db')
        return conn
    except Error as e:
        print(e)
        return None

def add_user_to_database(conn, user_id, first_name, last_name, username):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (id, first_name, last_name, username) VALUES (?, ?, ?, ?)",
                       (user_id, first_name, last_name, username))
        conn.commit()
    except Error as e:
        print(e)

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name or ''
    username = message.from_user.username or ''

    conn = create_connection()

    if conn:
        add_user_to_database(conn, user_id, first_name, last_name, username)
        conn.close()

    welcome_message = f"Привет👋🏻, {first_name} {last_name}!\nДобро пожаловать в мир творчества и креатива с нашим Telegram-ботом OverEdit!" \
                      f"\nМы готовы помочь вам воплотить ваши идеи в жизнь, предоставляя материалы для ваших редакторских проектов." \
                      f"\nНезависимо от того, создаете вы видеоролики, фотоколлажи или другие творческие контенты, мы здесь, чтобы сделать ваш процесс редактирования проще и вдохновляющим."

    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Помощь❓", callback_data='help')
    button2 = types.InlineKeyboardButton("Категории📋", callback_data='categories')
    button3 = types.InlineKeyboardButton("Избранное❤", callback_data='suggestion')

    markup.row(button1, button2, button3)

    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)

#------------------------------------------------------#     
#               Обработка нажатия кнопок               #            
#------------------------------------------------------#  
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'help':
        markup = create_back_keyboard()
        bot.send_message(call.message.chat.id, "Вы выбрали Помощь❓ \n✦ Если вы хотите посмотреть видео нажмите на кнопку Категории📋"\
                         f"\n✦ Если вы хотите переключить видео нажмите на кнопку 'Вперед'"\
                         f"\n✦ Если вы хотите посмотреть предыдущее видео, то нажмите на кнопку 'Назад'"\
                         f"\n✦ Если вам понравилось данное видео и вы хотите его добавить в избранное, то нажмите на кнопку 'Добавить в избранное'"
                         f"\n✦ Чтобы посмотреть избранные видео нажмите на кнопку Избранное❤",
                         reply_markup=markup)
        bot.answer_callback_query(call.id, text="", show_alert=False)


    elif call.data == 'Back':
        start(call.message)     
        bot.answer_callback_query(call.id, text="", show_alert=False)

    elif call.data == 'categories':

        inline_markup = types.InlineKeyboardMarkup()
        button_video = types.InlineKeyboardButton("Видео🎞️", callback_data='Video')
        button_back = types.InlineKeyboardButton("Назад", callback_data='Back')
        
        inline_markup.row(button_video)
        inline_markup.row(button_back)

        bot.send_message(call.message.chat.id, "Выберите тип оверлея.", reply_markup=inline_markup)
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False)


    elif call.data == 'Video':
        inline_markup = types.InlineKeyboardMarkup()
        button_theme1 = types.InlineKeyboardButton("Бабочки🦋", callback_data='Theme1')
        button_theme2 = types.InlineKeyboardButton("Звезды✨", callback_data='Theme2')
        button_theme3 = types.InlineKeyboardButton("Фон🌌", callback_data='Theme3')
        button_back_to_categories = types.InlineKeyboardButton("Назад к выбору категории", callback_data='BackToCategories')

        inline_markup.row(button_theme1, button_theme2, button_theme3)
        inline_markup.row(button_back_to_categories)

        bot.send_message(call.message.chat.id, "Выберите тематику оверлея.", reply_markup=inline_markup)
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False)
        

    elif call.data == 'Video_f':
        inline_markup = types.InlineKeyboardMarkup()
        button_theme1 = types.InlineKeyboardButton("Бабочки🦋", callback_data='Theme1_f')
        button_theme2 = types.InlineKeyboardButton("Звезды✨", callback_data='Theme2_f')
        button_theme3 = types.InlineKeyboardButton("Фон🌌", callback_data='Theme3_f')
        button_back_to_categories = types.InlineKeyboardButton("Назад к выбору категории", callback_data='BackToCategories')

        inline_markup.row(button_theme1, button_theme2, button_theme3)
        inline_markup.row(button_back_to_categories)

        bot.send_message(call.message.chat.id, "Выберите тематику оверлея.", reply_markup=inline_markup)
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False)

    elif call.data == 'BackToCategories':
        inline_markup = types.InlineKeyboardMarkup()
        button_video = types.InlineKeyboardButton("Видео🎞️", callback_data='Video')
        button_back = types.InlineKeyboardButton("Назад", callback_data='Back')

        inline_markup.row(button_video)
        inline_markup.row(button_back)

        bot.send_message(call.message.chat.id, "Выберите тип оверлея.", reply_markup=inline_markup)
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False)

#---------------------------------------------------------------------------------#     
#               Обработка нажатия кнопки "Назад к выбору категории"               #            
#---------------------------------------------------------------------------------# 
    elif call.data == 'BackToTheme':
        inline_markup = types.InlineKeyboardMarkup()
        button_theme1 = types.InlineKeyboardButton("Бабочки🦋", callback_data='Theme1')
        button_theme2 = types.InlineKeyboardButton("Звезды✨", callback_data='Theme2')
        button_theme3 = types.InlineKeyboardButton("Фон🌌", callback_data='Theme3')
        button_back_to_categories = types.InlineKeyboardButton("Назад к выбору категории", callback_data='BackToCategories')

        inline_markup.row(button_theme1, button_theme2, button_theme3)
        inline_markup.row(button_back_to_categories)

        bot.send_message(call.message.chat.id, "Выберите тематику оверлея.", reply_markup=inline_markup)
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False)


    elif call.data == 'NextVideo':
        if len(bot.videos) > 0:
            bot.current_video_index = (bot.current_video_index + 1) % len(bot.videos)
            markup = create_back_to_theme_keyboard()
            markup.add(types.InlineKeyboardButton("Добавить в избранное", callback_data='AddToFavorites'))
            send_video(call.message.chat.id, bot.videos[bot.current_video_index][1], markup,
                        bot.current_theme, bot.user_id, call.message.message_id)
            bot.answer_callback_query(call.id, text="", show_alert=False)

    elif call.data == 'PrevVideo':
        if len(bot.videos) > 0:
            bot.current_video_index = (bot.current_video_index - 1) % len(bot.videos)
            send_video(call.message.chat.id, bot.videos[bot.current_video_index][1], create_back_to_theme_keyboard_FAW(),
                        bot.current_theme, bot.user_id, call.message.message_id)
            bot.answer_callback_query(call.id, text="", show_alert=False)

    elif call.data == 'NextVideo_f':
        if len(bot.videos) > 0:
            bot.current_video_index = (bot.current_video_index + 1) % len(bot.videos)
            markup = create_back_to_theme_keyboard_FAW()
            send_video(call.message.chat.id, bot.videos[bot.current_video_index][1], markup,
                        bot.current_theme, bot.user_id, call.message.message_id)
            bot.answer_callback_query(call.id, text="", show_alert=False)

    elif call.data == 'PrevVideo_f':
        if len(bot.videos) > 0:
            bot.current_video_index = (bot.current_video_index - 1) % len(bot.videos)
            send_video(call.message.chat.id, bot.videos[bot.current_video_index][1], create_back_to_theme_keyboard_FAW(),
                        bot.current_theme, bot.user_id, call.message.message_id)
            bot.answer_callback_query(call.id, text="", show_alert=False)
 
#-----------------------------------------------------------------------#     
#              Обработка нажатия кнопки "добавить в избранное"          #            
#-----------------------------------------------------------------------# 
    elif call.data == 'suggestion':
        markup = create_favorite_keyboard_MENU2()
        bot.send_message(call.message.chat.id, "Выберите тип добавленного оверлея", reply_markup=markup)
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False)
                    
#--------------------------------------------------------------#     
#              Обработка нажатия кнопки "Бабочки"              #            
#--------------------------------------------------------------# 
    elif call.data == 'Theme1':
        conn = create_connection()

        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, file_url FROM overlays WHERE theme = 'Butterflies' AND type = 'video'")
                videos = cursor.fetchall()

                if videos:
                    bot.videos = videos
                    bot.current_theme = 'Butterflies'
                    markup = create_back_to_theme_keyboard()
                    markup.add(types.InlineKeyboardButton("Добавить в избранное", callback_data='AddToFavorites'))
                    send_video(call.message.chat.id, bot.videos[bot.current_video_index][1], markup)
                    bot.answer_callback_query(call.id, text="", show_alert=False)
            finally:
                cursor.close()
                conn.close()


    elif call.data == 'Theme1_f':
        conn = create_connection()

        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, file_url FROM overlays WHERE theme = 'Butterflies' AND type = 'video' AND favorite = 1")
                videos = cursor.fetchall()

                if videos:
                    bot.videos = videos
                    bot.current_theme = 'Butterflies'
                    markup = create_back_to_theme_keyboard_FAW()
                    send_video(call.message.chat.id, bot.videos[bot.current_video_index][1], markup)
                    bot.answer_callback_query(call.id, text="", show_alert=False)
                else:
                    bot.send_message(call.message.chat.id, "Нет избранных видео с темой 'Бабочки'")
            finally:
                cursor.close()
                conn.close()

#-----------------------------------------------#     
#       Обработка нажатия кнопки "Звезды"       #                     
#-----------------------------------------------#  

    elif call.data == 'Theme2':
        conn = create_connection()

        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, file_url FROM overlays WHERE theme = 'Sparkles' AND type = 'video'")
                videos = cursor.fetchall()

                # Проверяем, есть ли видео
                if videos:

                    bot.videos = videos
                    bot.current_theme = 'Sparkles'
                    markup = create_back_to_theme_keyboard()
                    markup.add(types.InlineKeyboardButton("Добавить в избранное", callback_data='AddToFavorites'))
                    send_video(call.message.chat.id, bot.videos[bot.current_video_index][1], markup)
                    bot.answer_callback_query(call.id, text="", show_alert=False)
            finally:
                cursor.close()
                conn.close()

  
    elif call.data == 'Theme2_f':
        conn = create_connection()

        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, file_url FROM overlays WHERE theme = 'Sparkles' AND type = 'video' AND favorite = 1")
                videos = cursor.fetchall()

                if videos:

                    bot.videos = videos
                    bot.current_theme = 'Sparkles'
                    markup = create_back_to_theme_keyboard_FAW()
                    send_video(call.message.chat.id, bot.videos[bot.current_video_index][1], markup)
                    bot.answer_callback_query(call.id, text="", show_alert=False)
                else:
                    bot.send_message(call.message.chat.id, "Нет избранных видео с темой 'Бабочки'")
            finally:
                cursor.close()
                conn.close()

#-----------------------------------------------#     
#       Обработка нажатия кнопки "Фон"          #                  
#-----------------------------------------------#      
                
    elif call.data == 'Theme3':
        conn = create_connection()

        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, file_url FROM overlays WHERE theme = 'Background' AND type = 'video'")
                videos = cursor.fetchall()

                if videos:
                    bot.videos = videos
                    bot.current_theme = 'Background'
                    markup = create_back_to_theme_keyboard()
                    markup.add(types.InlineKeyboardButton("Добавить в избранное", callback_data='AddToFavorites'))
                    send_video(call.message.chat.id, bot.videos[bot.current_video_index][1], markup)
                    bot.answer_callback_query(call.id, text="", show_alert=False)
            finally:
                cursor.close()
                conn.close()

 
    elif call.data == 'Theme3_f':
        conn = create_connection()

        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, file_url FROM overlays WHERE theme = 'Background' AND type = 'video' AND favorite = 1")
                videos = cursor.fetchall()

                if videos:
                    bot.videos = videos
                    bot.current_theme = 'Background'
                    markup = create_back_to_theme_keyboard_FAW()
                    send_video(call.message.chat.id, bot.videos[bot.current_video_index][1], markup)
                    bot.answer_callback_query(call.id, text="", show_alert=False)
                else:
                    bot.send_message(call.message.chat.id, "Нет избранных видео с темой 'Бабочки'")
            finally:
                cursor.close()
                conn.close()

 
#------------------------------------------------------#     
#     Обработка нажатия кнопки "Добавить в избранное"  #                         
#------------------------------------------------------#         
    elif call.data == 'AddToFavorites':
        conn = create_connection()

        if conn:
            try:
                cursor = conn.cursor()
                video_url = bot.videos[bot.current_video_index][1]
                cursor.execute("SELECT id FROM overlays WHERE file_url = ? AND favorite = 1", (video_url,))
                already_favorited = cursor.fetchone()

                if already_favorited:
                    bot.send_message(call.message.chat.id, "Это видео уже добавлено в избранное!")
                else:
                    cursor.execute("UPDATE overlays SET favorite = 1 WHERE file_url = ?", (video_url,))
                    conn.commit()
                    bot.send_message(call.message.chat.id, "Видео добавлено в избранное!")

                    markup = create_back_to_theme_keyboard()
                    markup.add(types.InlineKeyboardButton("Удалить из избранного", callback_data='RemoveFromFavorites'))
                    send_video(call.message.chat.id, video_url, markup, bot.current_theme, bot.user_id, call.message.message_id)
            finally:
                cursor.close()
                conn.close()

#------------------------------------------------------#     
#     Обработка нажатия кнопки "Удалить из избранного" #                          
#------------------------------------------------------#   
    elif call.data == 'RemoveFromFavorites':
        conn = create_connection()

        if conn:
            try:
                cursor = conn.cursor()
                video_url = bot.videos[bot.current_video_index][1]
                cursor.execute("SELECT id FROM overlays WHERE file_url = ? AND favorite = 0", (video_url,))
                already_removed = cursor.fetchone()

                if already_removed:
                    bot.send_message(call.message.chat.id, "Это видео уже удалено из избранного!")
                else:
                    cursor.execute("UPDATE overlays SET favorite = 0 WHERE file_url = ?", (video_url,))
                    conn.commit()
                    bot.send_message(call.message.chat.id, "Видео удалено из избранного!")

                    markup = create_back_to_theme_keyboard()
                    markup.add(types.InlineKeyboardButton("Добавить в избранное", callback_data='AddToFavorites'))

                    send_video(call.message.chat.id, video_url, markup, bot.current_theme, bot.user_id, call.message.message_id)
            finally:
                cursor.close()
                conn.close()

#--------------------------------#     
#     Функция отправки видео     #                      
#--------------------------------#  
def send_video(chat_id, video_url, markup, theme=None, user_id=None, message_id=None):
    caption = f"Видео с темой {theme}" if theme else None
    
    if message_id:
        bot.edit_message_media(chat_id=chat_id, message_id=message_id,
                               media=types.InputMediaVideo(video_url, caption=caption), reply_markup=markup)
    else:
        bot.send_video(chat_id, video_url, caption=caption, reply_markup=markup)

    if user_id and theme:
        conn = create_connection()

        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO user_overlays (user_id, overlay_id) VALUES (?, ?)",
                               (user_id, bot.videos[bot.current_video_index][0]))
                conn.commit()
            finally:
                cursor.close()
                conn.close()

#--------------------------------------------#     
#     Функция отправки видео в избранное     #                      
#--------------------------------------------#            
def send_favorite_videos(chat_id, user_id):
    conn = create_connection()

    if conn:
        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT o.file_url
                FROM user_overlays uo
                INNER JOIN overlays o ON uo.overlay_id = o.id
                WHERE uo.user_id = ? AND o.favorite = 1
            """, (user_id,))
            favorite_videos = cursor.fetchall()

            if favorite_videos:

                markup = create_back_to_theme_keyboard()
                markup.add(types.InlineKeyboardButton("Добавить в избранное", callback_data='AddToFavorites'))
                for video_url in favorite_videos:
                    send_video(chat_id, video_url[0], markup, "Избранное", user_id)
            else:
                bot.send_message(chat_id, "В вашем избранном пока нет видео.")
        finally:
            cursor.close()
            conn.close()

def create_back_keyboard():
    markup = types.InlineKeyboardMarkup()
    button4 = types.InlineKeyboardButton("Назад", callback_data='Back')
    markup.row(button4)
    return markup

def create_back_to_categories_keyboard():
    markup = types.InlineKeyboardMarkup()
    button_back_to_categories = types.InlineKeyboardButton("Назад к выбору категории", callback_data='BackToCategories')
    markup.row(button_back_to_categories)
    return markup
 
def create_favorite_keyboard1():
    markup = types.InlineKeyboardMarkup()
    button_theme1 = types.InlineKeyboardButton("Бабочки🦋", callback_data='Theme1_f')
    button_theme2 = types.InlineKeyboardButton("Звезды✨", callback_data='Theme2_f')
    button_theme3 = types.InlineKeyboardButton("Фон🌌", callback_data='Theme3_f')
    button_back_to_categories = types.InlineKeyboardButton("Назад к выбору категории", callback_data='BackToCategories')
    markup.row(button_theme1)
    markup.row(button_theme2)
    markup.row(button_theme3)
    markup.row(button_back_to_categories)
    return markup

def create_back_to_theme_keyboard():
    markup = types.InlineKeyboardMarkup()
    button_back_to_theme = types.InlineKeyboardButton("Назад к выбору темы", callback_data='BackToTheme')
    button_prev_video = types.InlineKeyboardButton("Назад", callback_data='PrevVideo')
    button_next_video = types.InlineKeyboardButton(f"{bot.current_video_index + 1}/{len(bot.videos)} Вперед", callback_data='NextVideo')
    markup.row(button_back_to_theme)
    markup.row(button_prev_video, button_next_video)
    return markup

def create_back_to_theme_keyboard_FAW():
    markup = types.InlineKeyboardMarkup()
    button_back_to_theme = types.InlineKeyboardButton("Назад к выбору темы", callback_data='BackToTheme')
    button_prev_video = types.InlineKeyboardButton("Назад", callback_data='PrevVideo_f')
    button_next_video = types.InlineKeyboardButton(f"{bot.current_video_index + 1}/{len(bot.videos)} Вперед", callback_data='NextVideo_f')
    markup.row(button_back_to_theme)
    markup.row(button_prev_video, button_next_video)
    return markup

def create_favorite_keyboard_MENU2():
    markup = types.InlineKeyboardMarkup()
    button_video = types.InlineKeyboardButton("Видео🎞️", callback_data='Video_f')
    button_back = types.InlineKeyboardButton("Назад", callback_data='Back')
    markup.row(button_video)
    markup.row(button_back)
    return markup

def create_favorite_keyboard():
    markup = types.InlineKeyboardMarkup()
    button_video = types.InlineKeyboardButton("Видео🎞️", callback_data='Video')
    button_picture = types.InlineKeyboardButton("Картинки🌆", callback_data='Picture')
    button_back = types.InlineKeyboardButton("Назад", callback_data='Back')
    markup.row(button_video, button_picture, button_back)
    return markup

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Error: {e}")
