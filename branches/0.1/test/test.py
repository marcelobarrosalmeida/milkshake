import rtm

apiKey = "c1a983bba360889c5089d5ccf1a94e4a"
secret = "67b5855d779f0d37"
token = "ad9ce7ad7956bbf1a02ae6a8963085025a800472"

ms = rtm.RTM(apiKey, secret, token)

authURL = ms.getAuthURL()
print authURL
raw_input('Press enter once you gave access')
token = ms.getToken()

print "Token", token
