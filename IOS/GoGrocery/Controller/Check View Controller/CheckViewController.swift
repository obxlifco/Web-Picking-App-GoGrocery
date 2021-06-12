//
//  CheckViewController.swift
//  GoGrocery
//
//  Created by NAV63 on 20/07/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
import CCAvenueSDK
class CheckViewController: UIViewController ,CCAvenuePaymentControllerDelegate {
   

    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }
    

    @IBAction func btnCheckAction(_ sender: Any) {
       MakeDemoPayment()
    }
    
    func MakeDemoPayment() {
        
        
                       // MARK:- Merchant Id Live/Demo
                       let merchantIDTF = "43366" //Demo
                       // self.merchantIDTF = "46319" //Live
        
                         // MARK:- Acces Key Live/Demo
                        let acessCodeTF = "AVCG03HF47CJ43GCJC" //Demo
                      //  self.acessCodeTF = "AVZO03HA32BC46OZCB" //Live
        
                          // MARK:- Currency Live/Demo
                       // let currencyTF = "AED"
        
                        // MARK:- Redirect url Live/Demo
                         let redirectURLTF = "http://15.185.126.44:8062/api/front/v1/payment-response/" //Demo1
                         // let cancelURLTF = "http://15.185.126.44:8062/api/front/v1/payment-res/" //Demo1
        
                      //  self.redirectURLTF = "https://www.gogrocery.ae/api/front/v1/payment-res/" //Live
                     //   self.cancelURLTF = "https://www.gogrocery.ae/api/front/v1/payment-res/" //Live
          let rsaKeyURLTF = "https://www.gogrocery.ae/api/front/v1/get-rsa-demo/" //Demo1
        
        let paymentController = CCAvenuePaymentController.init(orderId:"\((arc4random() % 9999999) + 1)" ,
                                                               merchantId:merchantIDTF ,
                                                               accessCode:acessCodeTF,
                                                               custId:"1234",
                                                               amount:"10",
                                                               currency:"AED",
                                                               rsaKeyUrl:rsaKeyURLTF,
                                                               redirectUrl:redirectURLTF,
                                                               cancelUrl:redirectURLTF,
                                                               showAddress:"Y",
                                                               billingName:"ABC",
                                                               billingAddress:"Star City",
                                                               billingCity:"Dubai",
                                                               billingState:"Dubai",
                                                               billingCountry:"United Arab Emirates",
                                                               billingTel:"+971 1234567890",
                                                               billingEmail:"test@gmail.com" ,
                                                               deliveryName:"XYZ",
                                                               deliveryAddress:"Internet City",
                                                               deliveryCity:"Dubai",
                                                               deliveryState:"Dubai",
                                                               deliveryCountry:"United Arab Emirates",
                                                               deliveryTel:"+971 9876543210",
                                                               promoCode:"" ,
                                                               merchant_param1:"Param 1",
                                                               merchant_param2:"Param 2",
                                                               merchant_param3:"Param 3",
                                                               merchant_param4:"Param 4" ,
                                                               merchant_param5:"Param 5",
                                                               useCCPromo:"Y",
                                                               siType:"ONDEMAND",
                                                               siMerchantRefNo:"1234",
                                                               siSetupAmount: "Y",
                                                               siAmount: "1",
                                                               siStartDate: "20-07-2020",
                                                               siFrequencyType: "",
                                                               siFrequency: "",
                                                               siBillCycle: ""
        )
         paymentController?.delegate = self;
         self.present(paymentController!, animated: true, completion: nil);
    }
 func getResponse(_ responseDict_: NSMutableDictionary!) {
        print(responseDict_)
    }
    

}
