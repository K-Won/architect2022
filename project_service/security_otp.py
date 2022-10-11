import pyotp
import datetime

def check_otp():
    otp_key = 'GAYDAMBQGAYDAMBQGAYDAMBQGA======'
    totp = pyotp.TOTP(otp_key)
    now = datetime.datetime.now()

    print('current time : ', now)
    print("now totp.at: " + str(totp.at(datetime.datetime.now())) + ", totp.now : " + totp.now())
    print('next otp : ', totp.at(int(now.timestamp()) + (5 * 60 + 30)))

    return totp.now()



if __name__ == '__main__':
    totp = check_otp()
    print(totp)
