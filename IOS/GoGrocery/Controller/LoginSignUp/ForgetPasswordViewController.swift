//
//  ForgetPasswordViewController.swift
//  GoGrocery
//
//  Created by BMS-09-M on 24/12/19.
//  Copyright © 2019 BMS-09-M. All rights reserved.
//

import UIKit
import SwiftyJSON
class ForgetPasswordViewController: UIViewController,UITextFieldDelegate {

    @IBOutlet weak var btnSendResetLink: UIButton!
    @IBOutlet weak var txtEmail: UITextField!
    @IBOutlet weak var lblEmail: UILabel!
    override func viewDidLoad() {
        super.viewDidLoad()

        emailtxtInActive()
        txtEmail.delegate = self
        btnSendResetLink.layer.cornerRadius = 5
        txtEmail.setLeftPaddingPoints(10)
        txtEmail.layer.cornerRadius = 5
        self.navigationController?.isNavigationBarHidden = false
        self.title = "Forget Password"
        UINavigationBar.appearance().tintColor = UIColor.black //your desired color here
        // Do any additional setup after loading the view.
    }
    
    func emailtxtActive() {
        self.txtEmail.layer.borderColor = UIColor(named: "textBorderColor")?.cgColor
        self.txtEmail.layer.borderWidth = 1
        self.lblEmail.isHidden = false
    }
    func emailtxtInActive() {
        txtEmail.layer.borderColor = UIColor.darkGray.cgColor
        txtEmail.layer.borderWidth = 1
        self.lblEmail.isHidden = true
    }
    @IBAction func btnSendResetLinkAction(_ sender: Any) {
      if txtEmail.text!.trimmingCharacters(in: .whitespaces).isEmpty {
            createalert(title: "Alert", message: "Please enter email or phone number", vc: self)
        }
      else {
        ApiCallToResendLink()
        }
    }
    func textFieldDidBeginEditing(_ textField: UITextField) {
           if textField == txtEmail {
               emailtxtActive()
           }
    }
    func textFieldDidEndEditing(_ textField: UITextField, reason: UITextField.DidEndEditingReason) {
        if textField == txtEmail {
            emailtxtInActive()
         
    }
    }
    
    func  ApiCallToResendLink() {
        var params = [String:Any]()
        params["email"] = self.txtEmail.text
        postMethodSocialSignIn(apiName: "forgotpassword/", params: params, vc: self) { (response : JSON) in
            if response["status"].intValue == 1 {
            let msg = response["message"].stringValue
            self.showAlert(message: msg)
            }
            else {
                createalert(title: "Alert", message: "This email does not exist", vc: self)
            }
        }
    }
    //    MARK:- Alert
    func showAlert(message: String)
    {
        let alert = UIAlertController(title: "Success", message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .default, handler: { (_) in
            self.navigationController?.popViewController(animated: true)
        }))
        self.present(alert, animated: true, completion: nil)
    }
}

