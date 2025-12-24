import xmlschema

schema = xmlschema.XMLSchema("resource/pacs008.xsd")
pacs8="""<?xml version="1.0" encoding="UTF-8"?>

<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08">
    <FIToFICstmrCdtTrf>
        <GrpHdr>
            <MsgId>MSGID-20230101-001</MsgId>
            <CreDtTm>2023-01-01T10:00:00+08:00</CreDtTm>
            <NbOfTxs>1</NbOfTxs>
            <SttlmInf>
                <SttlmMtd>CLRG</SttlmMtd>
                <ClrSys>
                    <Cd>MEP</Cd>
                </ClrSys>
            </SttlmInf>
        </GrpHdr>
        <CdtTrfTxInf>
            <PmtId>
                <InstrId>INSTRID001</InstrId>
                <EndToEndId>E2EID-ABC-12345</EndToEndId>
                <UETR>f47ac10b-58cc-4372-a567-0e02b2c3d479</UETR>
            </PmtId>
            <PmtTpInf>
                <SvcLvl>
                    <Cd>URGP</Cd>
                </SvcLvl>
            </PmtTpInf>
            <IntrBkSttlmAmt Ccy="SGD">1000.00</IntrBkSttlmAmt>
            <IntrBkSttlmDt>2023-01-02</IntrBkSttlmDt>
            <ChrgBr>SHAR</ChrgBr>
            <InstgAgt>
                <FinInstnId>
                    <BICFI>BANKXXS1XXX</BICFI>
                    <Nm>Instructing Bank One</Nm>
                </FinInstnId>
            </InstgAgt>
            <InstdAgt>
                <FinInstnId>
                    <BICFI>BANKYY22XXX</BICFI>
                    <Nm>Instructed Bank Two</Nm>
                </FinInstnId>
            </InstdAgt>
            <Dbtr>
                <Nm>John Doe</Nm>
                <Id>
                    <PrvtId>
                        <Othr>
                            <Id>PASSPORT12345</Id>
                            <SchmeNm>
                                <Cd>DRLC</Cd>
                            </SchmeNm>
                        </Othr>
                    </PrvtId>
                </Id>
            </Dbtr>
            <DbtrAcct>
                <Id>
                    <IBAN>SG68333333330000000001</IBAN>
                </Id>
            </DbtrAcct>
            <DbtrAgt>
                <FinInstnId>
                    <BICFI>BANKZZ33XXX</BICFI>
                    <Nm>Debtor Agent Bank</Nm>
                </FinInstnId>
            </DbtrAgt>
            <CdtrAgt>
                <FinInstnId>
                    <BICFI>BANKWW44XXX</BICFI>
                    <Nm>Creditor Agent Bank</Nm>
                </FinInstnId>
            </CdtrAgt>
            <Cdtr>
                <Nm>Jane Smith</Nm>
                <Id>
                    <OrgId>
                        <Othr>
                            <Id>ORGID67890</Id>
                            <SchmeNm>
                                <Cd>CUST</Cd>
                            </SchmeNm>
                        </Othr>
                    </OrgId>
                </Id>
            </Cdtr>
            <CdtrAcct>
                <Id>
                    <Othr>
                        <Id>7890123456</Id>
                        <SchmeNm>
                            <Prtry>AccountType</Prtry>
                        </SchmeNm>
                    </Othr>
                </Id>
            </CdtrAcct>
            <RmtInf>
                <Ustrd>Payment for services rendered.</Ustrd>
            </RmtInf>
             <RmtInf>
                <Ustrd>Payment for services rendered.</Ustrd>
            </RmtInf>
        </CdtTrfTxInf>
    </FIToFICstmrCdtTrf>
</Document>"""
bools=schema.is_valid(pacs8)

if(bools):
    print("valid")
else:
    schema.validate(pacs8)


