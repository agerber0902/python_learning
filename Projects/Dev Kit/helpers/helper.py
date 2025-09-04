from helpers.constants import ERROR_SYM, WARNING_SYM, SUCCESS_SYM, INFO_SYM

# Set Success Message
def setSuccessMessage(message):
    return f"{SUCCESS_SYM} {message}"

# Set Warning Message
def setWarningMessage(message):
    return f"{WARNING_SYM} {message}"

# Set Error Message
def setErrorMessage(message):
    return f"{ERROR_SYM} {message}"

# Set Info Message
def setInfoMessage(message):
    return f"{INFO_SYM} {message}"

# Print messages
def printSuccess(message):
    print(setSuccessMessage(message))
def printWarning(message):
    print(setWarningMessage(message))
def printError(message):
    print(setErrorMessage(message))
def printInfo(message):
    print(setInfoMessage(message))