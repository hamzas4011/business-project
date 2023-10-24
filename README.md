# business-project

This program shows a business management system by using two classes.
Business class represent business name, money available and dictionary to store items and
deals. Ware class has items with name and price. Furthermore, this Python program allows
the user to create a new business or manage existing ones, restocking items by decreasing available money
and increasing item quantities, checking item prices with deals, checking item availability,
sell items, add and remove deals, and quit the program.

So why did we use the pickle module?
The dictionary holding details about the business are stored in a file using pickle,
then it allows the program to load and save data between sessions.
