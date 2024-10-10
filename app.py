from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Initial values
user_data = {
    'balance': random.randrange(101),  # Random balance between 0 and 100
    'apples': 0,  # User starts with 0 apples
    'buy_price_per_apple': 5,  # Default price for buying apples
    'history': []  # Transaction history
}

# List of customer names
customers = ["Mr. Rogers", "Bob", "Sheriff Akangbe", "Diana", "Gbenga", "Frank", "Grace", "Hank"]

@app.route('/', methods=['GET', 'POST'])
def index():
    customer_name = None  # Variable to store the customer's name
    error_message = None  # Variable to store error messages
    message = None

    # Update the buy price dynamically (can fluctuate)
    def update_buy_price():
        return random.randint(3, 10)
    
    user_data['buy_price_per_apple'] = update_buy_price()
    min_sell_price = int(0.8 * user_data['buy_price_per_apple'])
    max_sell_price = int(1.7 * user_data['buy_price_per_apple'])

    if request.method == 'POST':
        action = request.form['action']  # Buy or Sell
        a_oa = int(request.form['apples'])  # Number of apples the user wants to buy/sell
        buy_price = user_data['buy_price_per_apple']
        
        if action == 'sell':
            custom_price = int(request.form['sell_price'])
            if custom_price < min_sell_price or custom_price > max_sell_price:
                error_message = f"Your selling price must be between {min_sell_price} and {max_sell_price} bucks per apple."
            else:
                cost = a_oa * custom_price
                if a_oa > user_data['apples']:
                    error_message = "You don't have enough apples to sell."
                else:
                    customer_name = random.choice(customers)
                    user_data['balance'] += cost
                    user_data['apples'] -= a_oa
                    message = f"You sold {a_oa} apples for {cost} bucks ({custom_price} bucks per apple) to {customer_name}. You now have {user_data['balance']} bucks."
                    user_data['history'].append(message)

        elif action == 'buy':
            cost = a_oa * buy_price
            if cost > user_data['balance']:
                error_message = "You don't have enough money to buy that many apples."
            else:
                user_data['balance'] -= cost
                user_data['apples'] += a_oa
                message = f"You bought {a_oa} apples for {cost} bucks. You now have {user_data['balance']} bucks left."
                user_data['history'].append(message)

    return render_template('index.html', 
                           error_message=error_message, 
                           message=message, 
                           l_initial=user_data['balance'], 
                           apples=user_data['apples'], 
                           buy_price=user_data['buy_price_per_apple'], 
                           min_sell_price=min_sell_price, 
                           max_sell_price=max_sell_price, 
                           customer_name=customer_name,
                           history=user_data['history'])

if __name__ == '__main__':
    app.run(debug=True)