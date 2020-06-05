Скрипт для регистрации терминалов на OLT ZTE C320. Для работы скрипта требуются модули pyhon:
pip install sys pexpect testfsm time date

Запуск скрипта осуществляется следующей коммандой:
python reg.py 172.16.1.250 gpon-onu_1/1/4

Можно добавить в крон на выполнение раз в 3 минуты:
*/3 * * * * root /home/user/scripts/reg.py python reg.py 172.16.1.250 gpon-onu_1/1/4 >> /home/user/scripts/reg.log 2>&1
