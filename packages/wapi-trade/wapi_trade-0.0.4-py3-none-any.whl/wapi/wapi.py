import cloudscraper
from bs4 import BeautifulSoup

class Trade:
    """
    Attributes
    ----------
    session: session
        Cloudscraper requests session that holds Wealthsimple session cookies and header information
    token: str
        Bearer authorization token used to validate each request
    client_id: str
        client id

    Methods
    -------
    login(email, password)
        Logs in to Wealthsimple Trade account
    switch()
        Switches authorization token to keep session alive, call this function every 20 minutes while the program is running
    get_account_id(account_type)
        Returns account id related to inputted account type: tfsa, rrsp, non-reg, cryto
    get_account_balance(account_type)
        Returns buying power of account related to inputted account type
    get_lastest_order(order_num=0)
        Returns information on the lastest order transacted
    get_order(order_id, orders=20)
        Returns information on the order with the inputted order id
    get_position()
        Returns dictonary containing information all current positions
    get_security_id(symbol)
        Returns security id of inputted ticker
    get_market_value(sec_id)
        Returns market value of ticker with the inputted security id
    get_market_status()
        Returns dictionary containing the market status of all exchanges used by Wealthsimple Trade
    place_market_order(symbol, side, account_type, shares)
        Places market order and returns order id
    place_limit_order(symbol, side, account_type, shares, price)
        Places limit order and returns order id
    cancel_order(order_id)
        Cancels order with inputted order id
    """
    def __init__(self, email, password):
        """
        Parameters
        ----------
        email: str
            Email used to login to Wealthsimple Trade
        password: str
            Password used to login to Wealthsimple Trade

        Returns
        -------
        None
        """
        self.session = self.login(email, password)

    def login(self, username, password):
        """
        Parameters
        ----------
        username: str
            Username used to login to Wealthsimple Trade
        password: str
            Password used to login to Wealthsimple Trade

        Returns
        -------
        session
            Cloudscraper session that is logged into Wealthsimple Trade
        """
        user_login_url = "https://my.wealthsimple.com/app/login"
        api_login_url = "https://api.production.wealthsimple.com/v1/oauth/token"
        switch_url = "https://api.production.wealthsimple.com/v1/oauth/switch"

        login_data = {
            "grant_type": "password",
            "otp_claim": None,
            "password": password,
            "scope": "invest.read invest.write mfda.read mfda.write mercer.read mercer.write trade.read trade.write empower.read empower.write tax.read tax.write",
            "skip_provision": True,
            "username": username
        }

        switch_data = {
            "profile": "trade",
            "scope": "invest.read invest.write trade.read trade.write tax.read tax.write"
        }

        with cloudscraper.CloudScraper() as session:
            session.headers.update({"Accept-Language": "en-CA,en-US;q=0.7,en;q=0.3"})
            response = session.get(user_login_url)

            soup = BeautifulSoup(response.content, "html.parser")
            id_url = str(soup.find_all("script")[5]).split("src=\"")[1].split("\"")[0]

            response = session.get(id_url)
            client_id = str(response.text).split("{env:\"production\",clientId:\"")[1].split("\"")[0]

            login_data["client_id"] = client_id
            switch_data["client_id"] = client_id
            self.client_id = client_id
            
            #SENDS THE 2FA EMAIL
            session.post(url=api_login_url, data=login_data)

            otp = input("OTP: ").strip()
            session.headers.update({"x-wealthsimple-otp": otp})

            response = session.post(url=api_login_url, data=login_data).json()
            session.headers.pop("x-wealthsimple-otp")

            self.token = f"{response['token_type']} {response['access_token']}"

            session.headers.update({"Authorization": self.token})
            response = session.post(url=switch_url, json=switch_data).json()

            self.token = f"{response['token_type']} {response['access_token']}"
            session.headers.update({"Authorization": self.token})

            return session

    def switch(self):
        """
        Returns
        -------
        None
        """
        switch_data = {
            "profile": "trade",
            "scope": "invest.read invest.write trade.read trade.write tax.read tax.write",
            "client_id": self.client_id
        }
        switch_url = "https://api.production.wealthsimple.com/v1/oauth/switch"

        response = self.session.post(url=switch_url, json=switch_data).json()
        
        self.token = f"{response['token_type']} {response['access_token']}"
        self.session.headers.update({"Authorization": self.token})

    def get_account_id(self, account_type):
        """
        Parameters
        ----------
        account_type: str
            Account type: i.e. tfsa, rrsp, non-reg(personal), crypto

        Returns
        -------
        str
            Account id associated with inputted account type
        """
        account_type = account_type.lower()

        response = self.session.get("https://trade-service.wealthsimple.com/me").json()["account_signatures"]

        for item in response:
            external_id = item["external_account_id"]
            if "crypto" in account_type:
                if account_type in external_id:
                    account_id = external_id
                    break
            else:
                if account_type in external_id and "crypto" not in external_id:
                    account_id = external_id
                    break

        return account_id

    def get_account_balance(self, account_type):
        """
        Parameters
        ----------
        account_type: str
            Account type: i.e. tfsa, rrsp, non-reg(personal), crypto

        Returns
        -------
        dict
            A dictionary containing both the account id and buying power associated with the inputted account type
        """
        account_id = self.get_account_id(account_type)

        response = self.session.get("https://trade-service.wealthsimple.com/account/list").json()["results"]

        for item in response:
            if account_id in item["id"]:
                account = {
                    "account_id": item["id"], 
                    "buying_power": item["buying_power"]["amount"]
                }

        return account

    def get_latest_order(self, order_num=0):
        """
        Parameters
        ----------
        order_num: int
            Order position in order list

        Returns
        -------
        dict
            A dictionary containing information about the order retrieved
        """
        response = self.session.get(f"https://trade-service.wealthsimple.com/account/activities?account_ids=&limit={order_num + 1}").json()["results"][order_num]
        
        if response["status"] == "posted":
            order = {
            "symbol": response["symbol"], 
            "order_id": response["id"],
            "order_type": response["order_type"], 
            "order_sub_type": response["order_sub_type"], 
            "status": response["status"], 
            "quantity": response["fill_quantity"], 
            "value": response["market_value"]["amount"]
            }
        elif response["status"] == "accepted":
            raise Exception("Error, Latest Activity Was Not A Trade")
        else:
            order = {
                "symbol": response["symbol"],
                "status": response["status"],
                "order_id": response["id"],
                "limit_price": response["limit_price"]["amount"]
            }

        return order
    def get_order(self, order_id, orders=20):
        """
        Parameters
        ----------
        order_id: str
            Order id of order being retrieved
        orders: int
            Amount of orders to load

        Returns
        -------
        dict
            A dictionary containing information about the order retrieved
        """
        response = self.session.get(f"https://trade-service.wealthsimple.com/account/activities?account_ids=&limit={orders}").json()["results"]
        for item in response:
            if item["id"] == order_id:
                if item["status"] == "posted":
                    order = {
                    "symbol": item["symbol"], 
                    "order_id": item["id"],
                    "order_type": item["order_type"], 
                    "order_sub_type": item["order_sub_type"], 
                    "status": item["status"], 
                    "quantity": item["fill_quantity"], 
                    "value": item["market_value"]["amount"]
                }
                else:
                    order = {
                        "symbol": item["symbol"],
                        "status": item["status"],
                        "order_id": item["id"],
                        "limit_price": item["limit_price"]["amount"]
                    }

        return order

    def get_position(self):
        """
        Returns
        -------
        dict
            A dictionary containing information on all positions currently being held
        """
        response = self.session.get(url="https://trade-service.wealthsimple.com/account/positions").json()["results"]

        pos_dict = {}
        for item in response:
            pos_dict[item["stock"]["symbol"]] = {
                    "name": item["stock"]["name"], 
                    "sec_id": item["id"],
                    "exchange": item["stock"]["primary_exchange"], 
                    "book_value": item["book_value"]["amount"],
                    "quantity": item["quantity"],
                    "buy_price": item["book_value"]["amount"] / item["quantity"],
                    "account_id": item["account_id"]
                }

        return pos_dict

    def get_security_id(self, symbol): 
        """
        Parameters
        ----------
        symbol: str
            Symbol used to get associated security id

        Returns
        -------
        str:
            Security id of inputted symbol
        """
        params = {
            "allow_ineligible_security": "false",
            "query": symbol
        }
        
        sec_id = self.session.get(url=f"https://trade-service.wealthsimple.com/securities", params=params).json()["results"][0]["id"]

        return sec_id

    def get_market_value(self, sec_id):

        market_value = self.session.get(url=f"https://trade-service.wealthsimple.com/securities/{sec_id}").json()["quote"]["amount"]

        return market_value

    def get_market_status(self):
        """
        Returns
        -------
        dict
            A dictionary containing the status of all stock exchanges used by Wealthsimple Trade
        """
        response = self.session.get(url="https://trade-service.wealthsimple.com/markets").json()["results"]

        markets = {}

        for item in response:
            if "open" in item:
                markets[item["exchange_name"]] = True
            else:
                markets[item["exchange_name"]] = False

        return markets

    def place_market_order(self, symbol, side, account_type, shares):
        """
        Parameters
        ----------
        symbol: str
            Symbol to buy/sell
        side: str
            Side of order; buy or sell
        account_type: str
            Account to use when placing order
        shares: int
            Number of shares to buy/sell

        Returns
        -------
        str
            Order id
        """
        sec_id = self.get_security_id(symbol)
        market_value = self.get_market_value(sec_id)

        post_data = {
            "account_id": self.get_account_id(account_type),
            "security_id": sec_id,
            "order_sub_type": "market",
            "time_in_force": "day",
            "market_value": market_value,
            "quantity": shares,
        }

        if side.lower() == "buy":
            post_data["order_type"] = "buy_quantity"
            post_data["limit_price"] = round(float(market_value) + float(market_value) * 0.05, 2)
            buying_power = self.get_account_balance(account_type)["buying_power"]

            if buying_power >= post_data["limit_price"] * shares:
                order_id = self.session.post(url="https://trade-service.wealthsimple.com/orders", json=post_data).json()["id"]
                return order_id
            else:
                raise Exception("Insufficient Funds")

        else:
            post_data["order_type"] = "sell_quantity"
            pos = self.get_position()

            if symbol in pos and pos[symbol]["quantity"] >= shares and account_type in pos[symbol]["account_id"] and "crypto" not in account_type:
                order_id = self.session.post(url="https://trade-service.wealthsimple.com/orders", json=post_data).json()["id"]
                return order_id

        raise Exception("Cannot Place Sell Order")

    def place_limit_order(self, symbol, side, account_type, shares, price):
        """
        Parameters
        ----------
        symbol: str
            Symbol to buy/sell
        side: str
            Side of order; buy or sell
        account_type: str
            Account to use when placing order
        shares: int
            Number of shares to buy/sell
        price: float
            Price to execute order at

        Returns
        -------
        str
            Order id
        """
        sec_id = self.get_security_id(symbol)

        post_data = {
            "account_id": self.get_account_id(account_type),
            "security_id": sec_id,
            "order_sub_type": "limit",
            "time_in_force": "until_cancel",
            "market_value": price,
            "quantity": shares,
            "limit_price": price
        }

        if side.lower() == "buy":
            post_data["order_type"] = "buy_quantity"
            buying_power = self.get_account_balance(account_type)["buying_power"]

            if buying_power >= post_data["limit_price"] * shares:
                order_id = self.session.post(url="https://trade-service.wealthsimple.com/orders", json=post_data).json()["id"]
                return order_id
            else:
                raise Exception("Insufficient Funds")

        else:
            post_data["order_type"] = "sell_quantity"
            pos = self.get_position()

            if symbol in pos and pos[symbol]["quantity"] >= shares and account_type in pos[symbol]["account_id"] and "crypto" not in account_type:
                order_id = self.session.post(url="https://trade-service.wealthsimple.com/orders", json=post_data).json()["id"]
                return order_id

        raise Exception("Cannot Place Sell Order")

    def cancel_order(self, order_id):
        """
        Parameters
        ----------
        order_id: str
            Id of order of order to cancel

        Returns
        -------
        None
        """
        self.session.delete(url=f"https://trade-service.wealthsimple.com/orders/{order_id}")