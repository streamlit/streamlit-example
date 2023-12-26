import smtplib
import pandas as pd
import openpyxl


from email.mime.text import MIMEText
# email 用于构建邮件内容
from email.header import Header
import streamlit as st

# 发信方的信息：发信邮箱，QQ邮箱授权码
# 方便起见，你也可以直接赋值
from_addr = ''
password = ''
smtp_server = ''

# 邮件内容
subject = '恭喜您获得读友会资格'
text_head = '''恭喜您获得读友会资格，
以下为您的读友会链接：

'''


def send_mail(receiver_list, message_list):
    st.divider()

    if smtp_server is None or \
            from_addr is None or \
            password is None:
        return
    else:
        print('--------------------')
        print(smtp_server, from_addr, password)

    try:
        receiver_num = len(receiver_list)

        for i in range(receiver_num):
            to_addr = receiver_list[i]
            message = text_head + message_list[i]

            msg = MIMEText(message, 'plain', 'utf-8')
            msg['From'] = Header(from_addr)
            msg['To'] = Header(to_addr)
            msg['Subject'] = Header(subject)

            server = smtplib.SMTP_SSL(smtp_server, 465)
            # server.set_debuglevel(0)
            server.connect(smtp_server, 465)
            server.login(from_addr, password)

            server.sendmail(from_addr, to_addr, msg.as_string())
            print(from_addr, to_addr, text_head)
            st.write(to_addr, " - Email sent successfully!")

    except Exception as e:
        st.write("An error occurred while sending the email:", str(e))

    finally:
        server.quit()


################## streamlit UI #########################
st.title('邮件发送助手')
tab1, tab2 = st.tabs(["发送设置", "发送邮件"])

with tab1:
    st.header("发送设置")

    smtp_server = st.text_input('请输入服务器地址：', value=smtp_server)
    from_addr = st.text_input('请输入邮箱地址：', value=from_addr)
    password = st.text_input('请输入密码：', value=password, type='default')
    print(smtp_server, from_addr, password)

with tab2:
    st.header("发送邮件")
    subject = st.text_input('邮件主题：', value=subject)
    text_head = st.text_area("邮件内容：", value=text_head)
    st.divider()

    uploaded_file = st.file_uploader("请选择接收人员名单文件")
    st.divider()
    if uploaded_file is not None:
        data = pd.read_excel(uploaded_file)
        receiver_address_list = data['邮箱']
        send_message_list = data['链接']
        if st.button("一键发送", type="primary", use_container_width=True):
            send_mail(receiver_address_list, send_message_list)
        st.dataframe(data, use_container_width=True)

###########################################

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # info_list = pd.read_excel(list_file)  # receiver address, message
    #
    # receiver_address_list = info_list['邮箱']
    # send_message_list = info_list['链接']

    # send_mail(receiver_address_list, send_message_list)
    i = 1
