//
//  ContactUsViewController.swift
//  GoGrocery
//
//  Created by NAV63 on 25/03/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
import SwiftyJSON
class ContactUsViewController: UIViewController {

    @IBOutlet weak var navigationView: UIView!
    @IBOutlet weak var btnSubmit: UIButton!
    @IBOutlet weak var btnCancel: UIButton!
    @IBOutlet weak var txtQuery: UITextView!
    @IBOutlet weak var lblQuery: UILabel!
    @IBOutlet weak var txtPhoneNumber: UITextField!
    @IBOutlet weak var lblPhoneNumber: UILabel!
    @IBOutlet weak var txtEmail: UITextField!
    @IBOutlet weak var lblEmail: UILabel!
    @IBOutlet weak var txtName: UITextField!
    @IBOutlet weak var lblName: UILabel!
    @IBOutlet weak var btnMail: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()

        allInActive1()
        txtName.delegate = self
        txtEmail.delegate = self
        txtPhoneNumber.delegate = self
        txtQuery.delegate = self
        
        txtName.layer.cornerRadius = 5
        txtEmail.layer.cornerRadius = 5
        txtPhoneNumber.layer.cornerRadius = 5
        txtQuery.layer.cornerRadius = 5
        
        
        txtName.setLeftPaddingPoints(10)
        txtEmail.setLeftPaddingPoints(10)
        txtPhoneNumber.setLeftPaddingPoints(10)
     //   txtQuery.setLeftPaddingPoints(10)
        txtQuery.textContainerInset = UIEdgeInsets(top: 5, left: 5, bottom: 0, right: 0)
        
        btnSubmit.layer.cornerRadius = 6
        btnSubmit.clipsToBounds = true
        btnSubmit.layer.borderWidth = 1
        btnSubmit.layer.borderColor = UIColor.red.cgColor
        
        btnCancel.layer.cornerRadius = 6
        btnCancel.clipsToBounds = true
        btnCancel.layer.borderWidth = 1
        btnCancel.layer.borderColor = UIColor.red.cgColor
     //   txtQuery.textColor = UIColor.lightGray
        navigationView.addShadow1()
        // Do any additional setup after loading the view.
    }
   
    @IBAction func btnPhoneContactAction(_ sender: Any) {
        let num = "+971600551685"
        guard let number = URL(string: "tel://" + num) else { return }
        UIApplication.shared.open(number)
    }
    
    @IBAction func btnMailAction(_ sender: Any) {
        let email = "support@gogrocery.ae"
        if let url = URL(string: "mailto:\(email)") {
          if #available(iOS 10.0, *) {
            UIApplication.shared.open(url)
          } else {
            UIApplication.shared.openURL(url)
          }
        }
    }
    
    @IBAction func btnSubmitAction(_ sender: Any) {
        if txtName.text!.trimmingCharacters(in: .whitespaces).isEmpty {
            createalert(title: "Alert", message: "Please enter your name", vc: self)
        }
        else if txtEmail.text!.trimmingCharacters(in: .whitespaces).isEmpty {
            createalert(title: "Alert", message: "Please enter your email", vc: self)
        }
        else if isValidEmail(testStr: txtEmail.text!) == false {
            createalert(title: "Alert", message: "Please enter valid email", vc: self)
        }
            else if txtPhoneNumber.text!.trimmingCharacters(in: .whitespaces).isEmpty {
                createalert(title: "Alert", message: "Please enter your phone number", vc: self)
            }
        else if txtQuery.text!.trimmingCharacters(in: .whitespaces).count < 5 {
            createalert(title: "Alert", message: "Please enter your query ", vc: self)
        }
        else {
            ApiCallToSubmit()
        }
    }
    
    @IBAction func btnCancelAction(_ sender: Any) {
        self.navigationController?.popViewController(animated: true)
    }
    
//    MARK:- Api Calling
    func  ApiCallToSubmit() {
        var params = [String:Any]()
        params["name"] = txtName.text!
        params["email"] = txtEmail.text!
        params["phone"] = txtPhoneNumber.text!
        params["message"] = txtQuery.text!
        print(params)
        postMethodQueryWithoutAuthorization(apiName: "customer-query/", params: params, vc: self) { (response : JSON) in
            print(response)
            if response["status"].intValue == 200 {
            self.showAlertOnContactUs(message: "Your query has been submitted")
            }
            else {
                createalert(title: "Alert", message: "Error in submitting query", vc: self)
            }
        }
        
    }
        func showAlertOnContactUs(message: String)
        {
            let alert = UIAlertController(title: "Success", message: message, preferredStyle: .alert)
            alert.addAction(UIAlertAction(title: "OK", style: .default, handler: { (_) in
                self.navigationController?.popViewController(animated: true)
                
            }))
            self.present(alert, animated: true, completion: nil)
        }
    
    //    MARK:- Active
      func NametxtActive() {
          self.txtName.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
          self.txtName.layer.borderWidth = 2
          self.lblName.isHidden = false
          self.lblName.textColor = UIColor(named: "buttonBackgroundColor")
      }
    
      func EmailtxtActive() {
          self.txtEmail.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
          self.txtEmail.layer.borderWidth = 2
          self.lblEmail.isHidden = false
          self.lblEmail.textColor = UIColor(named: "buttonBackgroundColor")
      }
      
      func MobiletxtActive() {
          self.txtPhoneNumber.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
          self.txtPhoneNumber.layer.borderWidth = 2
          self.lblPhoneNumber.isHidden = false
          self.lblPhoneNumber.textColor = UIColor(named: "buttonBackgroundColor")
      }
    func QuerytxtActive() {
        self.txtQuery.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.txtQuery.layer.borderWidth = 2
        self.lblQuery.isHidden = false
        self.lblQuery.textColor = UIColor(named: "buttonBackgroundColor")
    }
      
      //    MARK:- Inactive
      func NametxtInActive() {
          txtName.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
          txtName.layer.borderWidth = 2
          self.lblName.isHidden = true
      }
      func EmailtxtInActive() {
          txtEmail.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
          txtEmail.layer.borderWidth = 2
          self.lblEmail.isHidden = true
      }
      
      func MobiletxtInActive() {
          txtPhoneNumber.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
          txtPhoneNumber.layer.borderWidth = 2
          self.lblPhoneNumber.isHidden = true
      }
    func QuerytxtInActive() {
         txtQuery.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
         txtQuery.layer.borderWidth = 2
         self.lblQuery.isHidden = true
     }
    
    func allInActive1() {
        txtName.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtName.layer.borderWidth = 2
        self.lblName.isHidden = true
        
        txtEmail.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtEmail.layer.borderWidth = 2
        self.lblEmail.isHidden = true
        
        txtPhoneNumber.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtPhoneNumber.layer.borderWidth = 2
        self.lblPhoneNumber.isHidden = true
        
        txtQuery.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtQuery.layer.borderWidth = 2
        self.lblQuery.isHidden = true
    }
    
    
    @IBAction func btnBackaction(_ sender: Any) {
        self.navigationController?.popViewController(animated: true)
    }
    
    
}
extension ContactUsViewController : UITextFieldDelegate {
    func textFieldDidBeginEditing(_ textField: UITextField) {
        if textField == txtName {
            allInActive1()
            NametxtActive()
        }
        else if textField == txtEmail {
            allInActive1()
            EmailtxtActive()
        }
        else if textField == txtPhoneNumber {
            allInActive1()
            MobiletxtActive()
        }
    }
}
extension ContactUsViewController : UITextViewDelegate {
    func textViewDidBeginEditing(_ textView: UITextView) {
        if textView == txtQuery {
            allInActive1()
            QuerytxtActive()
        }
    }
}
