I and most of my colleagues often use the site olx.in for selling/buying used products at cheap prices. 
Whenever I contact a seller/buyer through chat, I get anxious about their response and find myself browsing the site more often than not. Missing few messages might lead to potential monetary loss.
To solve this problem, I wrote a notifier that'll check if there are any new messages in my olx account.
That way, I don't have to worry about missing out on messages any more!

Language: Python

Anyone who wants to use this, can do so by including a 'credentials.ini' file using the format of this [credentials file](sample_credentials.ini)

Edit1: Included logic to turn ON the LED pin on arduino board if the olx account has any unread messages.
Edit2: This project was initially written as a Jupyter notebook, later converted to .py file using python library nbconvert.
