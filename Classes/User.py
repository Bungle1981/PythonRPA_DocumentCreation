class User:
    def __init__(self, username="", firstName="", lastName="", address1="", address2="", town="", county="", postcode=""):
        self._userName = username
        self._firstName = firstName
        self._lastName = lastName
        self._address1 = address1
        self._address2 = address2
        self._town = town
        self._county = county
        self._postCode = postcode
        self._addressList = []

    def updateUser(self, updatedUser):
        self._firstName = updatedUser.returnFirstName()
        self._lastName = updatedUser.returnLastName()
        self._address1 = updatedUser.returnAddress1()
        self._address2 = updatedUser.returnAddress2()
        self._town = updatedUser.returnTown()
        self._county = updatedUser.returnCounty()
        self._postCode = updatedUser.returnPostcode()

    def returnUserName(self):
        return self._userName

    def returnFirstName(self):
        return self._firstName

    def returnLastName(self):
        return self._lastName

    def returnAddress1(self):
        return self._address1

    def returnAddress2(self):
        return self._address2

    def returnTown(self):
        return self._town

    def returnCounty(self):
        return self._county

    def returnPostcode(self):
        return self._postCode

    def returnAddressBlock(self):
        self._addressList = [self._address1, self._address2, self._town, self._county, self._postCode]
        return '\n'.join([str(item) for item in self._addressList if item != "" ])

    def returnUserSummary(self):
        return f"User name: {self.returnUserName()}, First name: {self.returnFirstName()}, Last name: {self.returnLastName()}, Post code: {self.returnPostcode()}"