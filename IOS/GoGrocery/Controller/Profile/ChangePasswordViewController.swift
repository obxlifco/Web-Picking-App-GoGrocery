//
//  ChangePasswordViewController.swift
//  GoGrocery
//
//  Created by Nav121 on 13/02/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
import SwiftyJSON
class ChangePasswordViewController: UIViewController {
    @IBOutlet weak var currentPasswordTxt: UITextField!
    @IBOutlet weak var currentPasswordLabel: UILabel!
    @IBOutlet weak var newPasswordTxt: UITextField!
    @IBOutlet weak var newPasswordLbl: UILabel!
    @IBOutlet weak var confirmPassTxt: UITextField!
    @IBOutlet weak var confirmPassLbl: UILabel!
    @IBOutlet weak var cancelBtn: UIButton!
    @IBOutlet weak var updateBtn: UIButton!
    @IBOutlet weak var currentPassImage: UIImageView!
    @IBOutlet weak var newPassImage: UIImageView!
    @IBOutlet weak var confirmPassImage: UIImageView!
    var isCurrentPassShow = false
    var isNewPassShow = false
    var isConfirmPassShow = false
    
    override func viewDidLoad() {
        super.viewDidLoad()
        allInActive1()
        currentPasswordTxt.delegate = self
        newPasswordTxt.delegate = self
        confirmPassTxt.delegate = self
        
        currentPasswordTxt.layer.cornerRadius = 5
        newPasswordTxt.layer.cornerRadius = 5
        confirmPassTxt.layer.cornerRadius = 5
        
        currentPasswordTxt.setLeftPaddingPoints(10)
        newPasswordTxt.setLeftPaddingPoints(10)
        confirmPassTxt.setLeftPaddingPoints(10)
        
        updateBtn.layer.cornerRadius = 6
        updateBtn.clipsToBounds = true
        updateBtn.layer.borderWidth = 1
        updateBtn.layer.borderColor = UIColor.red.cgColor
        
        cancelBtn.layer.cornerRadius = 6
        cancelBtn.clipsToBounds = true
        cancelBtn.layer.borderWidth = 1
        cancelBtn.layer.borderColor = UIColor.red.cgColor
    }
    
    override func viewWillAppear(_ animated: Bool) {
        self.navigationController?.isNavigationBarHidden = true
    }
    
    func newPasswordtxtTempActive() {
        self.newPasswordTxt.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        self.newPasswordTxt.layer.borderWidth = 2
        self.newPasswordLbl.isHidden = false
        self.newPasswordLbl.textColor = UIColor(named: "inactiveText")
    }
    func currentPasswordtxtTempActive() {
        self.currentPasswordTxt.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        self.currentPasswordTxt.layer.borderWidth = 2
        self.currentPasswordLabel.isHidden = false
        self.currentPasswordLabel.textColor = UIColor(named: "inactiveText")
    }
    
    func confirmPasstxtTempActive() {
        self.confirmPassTxt.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        self.confirmPassTxt.layer.borderWidth = 2
        self.confirmPassLbl.isHidden = false
        self.confirmPassLbl.textColor = UIColor(named: "inactiveText")
    }
    
    //    MARK:- Active
    func newPasswordtxtActive() {
        self.newPasswordTxt.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.newPasswordTxt.layer.borderWidth = 2
        self.newPasswordLbl.isHidden = false
        self.newPasswordLbl.textColor = UIColor(named: "buttonBackgroundColor")
    }
    func currentPasswordtxtActive() {
        self.currentPasswordTxt.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.currentPasswordTxt.layer.borderWidth = 2
        self.currentPasswordLabel.isHidden = false
        self.currentPasswordLabel.textColor = UIColor(named: "buttonBackgroundColor")
    }
    
    func confirmPasstxtActive() {
        self.confirmPassTxt.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.confirmPassTxt.layer.borderWidth = 2
        self.confirmPassLbl.isHidden = false
        self.confirmPassLbl.textColor = UIColor(named: "buttonBackgroundColor")
    }
    
    //    MARK:- Inactive
    func newPasswordtxtInActive() {
        newPasswordTxt.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        newPasswordTxt.layer.borderWidth = 2
        self.newPasswordLbl.isHidden = true
    }
    func currentPasswordtxtInActive() {
        currentPasswordTxt.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        currentPasswordTxt.layer.borderWidth = 2
        self.currentPasswordLabel.isHidden = true
    }
    
    func confirmPassInActive() {
        confirmPassTxt.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        confirmPassTxt.layer.borderWidth = 2
        self.confirmPassLbl.isHidden = true
    }
    
    func allInActive1() {
        newPasswordTxt.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        newPasswordTxt.layer.borderWidth = 2
        self.newPasswordLbl.isHidden = true
        
        currentPasswordTxt.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        currentPasswordTxt.layer.borderWidth = 2
        self.currentPasswordLabel.isHidden = true
        
        confirmPassTxt.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        confirmPassTxt.layer.borderWidth = 2
        self.confirmPassLbl.isHidden = true
        
    }
    @IBAction func showHideCurrentPassTapped(_ sender: Any) {
        
        
        if isCurrentPassShow == false {
            currentPasswordTxt.isSecureTextEntry = false
            isCurrentPassShow = true
            currentPassImage.image = UIImage(named: "showPassword")
        } else {
            currentPasswordTxt.isSecureTextEntry = true
            isCurrentPassShow = false
            currentPassImage.image = UIImage(named: "hidePassword")
        }
    }
    @IBAction func showHideNewPassTapped(_ sender: Any) {
        
        if isNewPassShow == false {
            isNewPassShow = true
            newPasswordTxt.isSecureTextEntry = false
            newPassImage.image = UIImage(named: "showPassword")
        } else {
            isNewPassShow = false
            newPasswordTxt.isSecureTextEntry = true
            newPassImage.image = UIImage(named: "hidePassword")
        }
    }
    @IBAction func showHideConfirmPassTapped(_ sender: Any) {
        
        if isConfirmPassShow == false {
            isConfirmPassShow = true
            confirmPassTxt.isSecureTextEntry = false
            confirmPassImage.image = UIImage(named: "showPassword")
        } else {
            isConfirmPassShow = false
            confirmPassTxt.isSecureTextEntry = true
            newPassImage.image = UIImage(named: "hidePassword")
        }
    }
    
    
    
    @IBAction func backButtonTapped(_ sender: Any) {
        self.navigationController?.popViewController(animated: true)
    }
    @IBAction func cancelBtnTapped(_ sender: Any) {
        self.navigationController?.popViewController(animated: true)
    }
    
    @IBAction func updateBtnTapped(_ sender: Any) {
        if currentPasswordTxt.text!.trimmingCharacters(in: .whitespaces).isEmpty {
            createalert(title: "Alert", message: "Please enter your current password", vc: self)
        }
        else if newPasswordTxt.text!.trimmingCharacters(in: .whitespaces).isEmpty {
            createalert(title: "Alert", message: "Please enter your new password", vc: self)
        }
        else if confirmPassTxt.text!.trimmingCharacters(in: .whitespaces).isEmpty {
            createalert(title: "Alert", message: "Please enter confirm password", vc: self)
        }
        else if newPasswordTxt.text! != confirmPassTxt.text! {
            createalert(title: "Alert", message: "Confirm password doesnt match", vc: self)
        }
        else if newPasswordTxt.text!.trimmingCharacters(in: .whitespaces).count < 5 {
            createalert(title: "Alert", message: "Minimum length of new password shoulb atleast 5 ", vc: self)
        }
        else {
            apiCallToUpdatepassword()
        }
    }
    
    func apiCallToUpdatepassword() {
        var params = [String:Any]()
        params["current_password"] = currentPasswordTxt.text!
        params["new_password"] = newPasswordTxt.text!
        params["confirm_password"] = confirmPassTxt.text!
        print(params)
        requestWithPut(methodName: "change-password/", parameter: params) { (response : JSON) in
            print(response)
            if response["status"].intValue == 200 {
                createalert(title: "Alert", message: "Password has been successfully updated", vc: self)
                self.currentPasswordTxt.text = ""
                self.newPasswordTxt.text = ""
                self.newPasswordTxt.text = ""
                // DispatchQueue.main.async {
                self.navigationController?.popViewController(animated: true)
                // }
            }
            else {
                let msg = response["message"].stringValue
                createalert(title: "Alert", message: msg, vc: self)
            }
        }
    }
}
extension ChangePasswordViewController : UITextFieldDelegate {
    func textFieldDidBeginEditing(_ textField: UITextField) {
        if textField == newPasswordTxt {
            allInActive1()
            newPasswordtxtActive()
        }
        else if textField == currentPasswordTxt {
            allInActive1()
            currentPasswordtxtActive()
        }
        else if textField == confirmPassTxt {
            allInActive1()
            confirmPasstxtActive()
        }
        
    }
    
    //TextField Validation
        func textField(_ textField: UITextField, shouldChangeCharactersIn range: NSRange, replacementString string: String) -> Bool  {
            if(textField == currentPasswordTxt)  {
                if range.location == 0 && string == " " {
                    return false
                }
                return true
            }
            else if(textField == newPasswordTxt)  {
                if range.location == 0 && string == " "
                {
                    return false
                }
                return true
            }
            else if(textField == confirmPassTxt) {
                if range.location == 0 && string == " "
                {
                    return false
                }
                return true
            }
            else {
                return true
            }
        }
}
