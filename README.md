# django-payments-worldpay
django-payments PayGate Backend (only basic authorization)

Quick and dirty work, no warranty, works for me.

### Quick Start

1. in settings
```
PAYMENT_VARIANTS = {
    'paygate': ('payments_paygate.PayGateProvider', {
        'pgid': '<your_pgid>',
        'pwd': '<your_pwd>',
    })
}
```

### Behavior

There are generally three types of response:

1. error - form error is available at __form.non_field_errors()__ using payment status ('error')
```
<protocol ver="4.0" pgid="10011021600" pwd="test" >
    <errorrx ecode="104" edesc="Card Not Accepted" />
</protocol>
```

2. declined - behavior is defined by custom template using payment status ('rejected')
```
<protocol ver="4.0" pgid="10011021600" pwd="test" >
    <authrx tid="32389988" cref="cust ref 1" stat="2" sdesc="Declined" res="900004" rdesc="Invalid Card Number" auth="00000000" bno="0" risk="XX" ctype="1" />
</protocol>
```

3. approved - tid is recorded and payment status is 'confirmed'
```
<protocol ver="4.0" pgid="10011021600" pwd="test" >
    <authrx tid="32389991" cref="cust ref 1" stat="1" sdesc="Approved" res="990017" rdesc="Auth Done" auth="00871445" bno="0" risk="XX" ctype="1" />
</protocol>
```