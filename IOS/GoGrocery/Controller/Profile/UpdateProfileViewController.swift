//
//  UpdateProfileViewController.swift
//  GoGrocery
//
//  Created by BMS-09-M on 31/12/19.
//  Copyright © 2019 BMS-09-M. All rights reserved.
//


import UIKit
import DropDown
import SwiftyJSON
class UpdateProfileViewController: UIViewController{
    //MARK:- Outlet Declaration
    @IBOutlet weak var imgImage: UIImageView!
    @IBOutlet weak var btnCamera: UIButton!
    @IBOutlet weak var txtFirstname: UITextField!
    @IBOutlet weak var lblFirstName: UILabel!
    @IBOutlet weak var txtLastName: UITextField!
    @IBOutlet weak var lblLastName: UILabel!
    @IBOutlet weak var txtEmail: UITextField!
    @IBOutlet weak var lblEmail: UILabel!
    @IBOutlet weak var txtMobile: UITextField!
    @IBOutlet weak var lblMobile: UILabel!
    @IBOutlet weak var txtGender: UITextField!
    @IBOutlet weak var lblGender: UILabel!
    @IBOutlet weak var txtAddress: UITextField!
    @IBOutlet weak var lblAddress: UILabel!
    @IBOutlet weak var btnCameraHeight: NSLayoutConstraint!
    @IBOutlet weak var lblCountryCode: UILabel!
    @IBOutlet weak var buttonCC: UIButton!
    @IBOutlet weak var lblCC: UILabel!
    @IBOutlet weak var mobileCCTable: UITableView!
    @IBOutlet weak var ccTableView: UIView!
    @IBOutlet weak var ccBackgroundView: UIView!
    //    MARK:- variable Declaration
    
    var maleSelect = Bool()
    var femaleSelect = Bool()
    var otherSelect = Bool()
    var selectedGender = String()
    var ccCode = ["50","52","53","54","55","56","58"]
    override func viewDidLoad() {
        super.viewDidLoad()
        
        ApiCallTogetUserDetails()
        allInActive1()
        txtFirstname.delegate = self
        txtLastName.delegate = self
        txtEmail.delegate = self
        txtMobile.delegate = self
        txtGender.delegate = self
        txtAddress.delegate = self
        
        txtFirstname.layer.cornerRadius = 5
        txtLastName.layer.cornerRadius = 5
        txtEmail.layer.cornerRadius = 5
        txtMobile.layer.cornerRadius = 5
        txtGender.layer.cornerRadius = 5
        txtAddress.layer.cornerRadius = 5
        
        txtFirstname.setLeftPaddingPoints(10)
        txtLastName.setLeftPaddingPoints(10)
        txtEmail.setLeftPaddingPoints(10)
        txtMobile.setLeftPaddingPoints(10)
        txtGender.setLeftPaddingPoints(10)
        txtAddress.setLeftPaddingPoints(10)
        imgImage.layer.cornerRadius = imgImage.layer.frame.height/2
        txtGender.addTarget(self, action: #selector(UpdateProfileViewController.textFieldDidChange(_:)), for: UIControl.Event.editingChanged)
        
        ccBackgroundView.alpha = 0
        ccTableView.alpha = 0
        lblCountryCode.layer.cornerRadius = 5
        lblCountryCode.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        lblCountryCode.layer.borderWidth = 2
        buttonCC.titleEdgeInsets.left = 10
        buttonCC.layer.cornerRadius = 5
        let tap = UITapGestureRecognizer(target: self, action: #selector(self.handleTap(_:)))
        ccBackgroundView.addGestureRecognizer(tap)
        // Do any additional setup after loading the view.
    }
    //    func ManageLayout() {
    //        switch(ch)
    //    }
    override func viewWillAppear(_ animated: Bool) {
        self.navigationController?.isNavigationBarHidden = false
        self.title = "Account Settings"
    }
    
    @IBAction func ccButtontapped(_ sender: Any) {
        ccActive()
        ccBackgroundView.alpha = 1
        ccTableView.alpha = 1
    }
    @objc func handleTap(_ sender: UITapGestureRecognizer? = nil) {
        print("handletap")
        ccInActive()
        UIView.animate(withDuration: 0.3, delay: 0.0, options: [], animations: {
            self.ccBackgroundView.alpha = 0
            self.ccTableView.alpha = 0
            
        })
    }
    func ccActive() {
        self.buttonCC.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.buttonCC.layer.borderWidth = 2
        if buttonCC.currentTitle == "CC" {
            self.buttonCC.setTitle("", for: .normal)
        }
        
        self.lblCC.isHidden = false
    }
    func ccInActive() {
        buttonCC.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        buttonCC.layer.borderWidth = 2
        if buttonCC.currentTitle == "" {
            self.buttonCC.setTitle("CC", for: .normal)
            self.buttonCC.setTitleColor(UIColor(named: "inactiveText"), for: .normal)
        }
        
        self.lblCC.isHidden = true
    }
    
    @objc func textFieldDidChange(_ textField: UITextField) {
        setUpGenderXibFunc ()
    }
    //    MARK:- Temp Active
    
    func firstNametxtTempActive() {
        self.txtFirstname.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        self.txtFirstname.layer.borderWidth = 2
        self.lblFirstName.isHidden = false
        self.lblFirstName.textColor = UIColor(named: "inactiveText")
    }
    func lastNametxtTempActive() {
        self.txtLastName.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        self.txtLastName.layer.borderWidth = 2
        self.lblLastName.isHidden = false
        self.lblLastName.textColor = UIColor(named: "inactiveText")
    }
    
    func emailtxtTempActive() {
        self.txtEmail.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        self.txtEmail.layer.borderWidth = 2
        self.lblEmail.isHidden = false
        self.lblEmail.textColor = UIColor(named: "inactiveText")
    }
    
    func mobiletxtTempActive() {
        self.txtMobile.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        self.txtMobile.layer.borderWidth = 2
        self.lblMobile.isHidden = false
        self.lblMobile.textColor = UIColor(named: "inactiveText")
    }
    func gendertxtTempActive() {
        self.txtGender.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        self.txtGender.layer.borderWidth = 2
        self.lblGender.isHidden = false
        self.lblGender.textColor = UIColor(named: "inactiveText")
    }
    func addresstxtTempActive() {
        self.txtAddress.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        self.txtAddress.layer.borderWidth = 2
        self.lblAddress.isHidden = false
        self.lblAddress.textColor = UIColor(named: "inactiveText")
    }
    
    
    //    MARK:- Active
    func firstNametxtActive() {
        self.txtFirstname.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.txtFirstname.layer.borderWidth = 2
        self.lblFirstName.isHidden = false
        self.lblFirstName.textColor = UIColor(named: "buttonBackgroundColor")
    }
    func lastNametxtActive() {
        self.txtLastName.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.txtLastName.layer.borderWidth = 2
        self.lblLastName.isHidden = false
        self.lblLastName.textColor = UIColor(named: "buttonBackgroundColor")
    }
    
    func emailtxtActive() {
        self.txtEmail.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.txtEmail.layer.borderWidth = 2
        self.lblEmail.isHidden = false
        self.lblEmail.textColor = UIColor(named: "buttonBackgroundColor")
    }
    
    func mobiletxtActive() {
        self.txtMobile.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.txtMobile.layer.borderWidth = 2
        self.lblMobile.isHidden = false
        self.lblMobile.textColor = UIColor(named: "buttonBackgroundColor")
    }
    func gendertxtActive() {
        self.txtGender.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.txtGender.layer.borderWidth = 2
        self.lblGender.isHidden = false
        self.lblGender.textColor = UIColor(named: "buttonBackgroundColor")
    }
    func addresstxtActive() {
        self.txtAddress.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.txtAddress.layer.borderWidth = 2
        self.lblAddress.isHidden = false
        self.lblAddress.textColor = UIColor(named: "buttonBackgroundColor")
    }
    
    //    MARK:- Inactive
    func firstNametxtInActive() {
        txtFirstname.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtFirstname.layer.borderWidth = 2
        self.lblFirstName.isHidden = true
    }
    func lastNametxtInActive() {
        txtLastName.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtLastName.layer.borderWidth = 2
        self.lblLastName.isHidden = true
    }
    
    func emailtxtInActive() {
        txtEmail.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtEmail.layer.borderWidth = 2
        self.lblEmail.isHidden = true
    }
    func mobiletxtInActive() {
        txtMobile.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtMobile.layer.borderWidth = 2
        self.lblMobile.isHidden = true
    }
    
    func genderInActive() {
        txtGender.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtGender.layer.borderWidth = 2
        self.lblGender.isHidden = true
    }
    func addressInActive() {
        txtAddress.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtAddress.layer.borderWidth = 2
        self.lblAddress.isHidden = true
    }
    //    MARK:- All Inactive
    func allInActive1() {
        txtFirstname.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtFirstname.layer.borderWidth = 2
        lblFirstName.isHidden = true
        
        txtLastName.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtLastName.layer.borderWidth = 2
        lblLastName.isHidden = true
        
        txtEmail.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtEmail.layer.borderWidth = 2
        lblEmail.isHidden = true
        
        txtMobile.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtMobile.layer.borderWidth = 2
        lblMobile.isHidden = true
        
        txtGender.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtGender.layer.borderWidth = 2
        lblGender.isHidden = true
        
        txtAddress.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        txtAddress.layer.borderWidth = 2
        lblAddress.isHidden = true
        
        buttonCC.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        buttonCC.layer.borderWidth = 2
        if buttonCC.currentTitle == "" {
            self.buttonCC.setTitle("CC", for: .normal)
            self.buttonCC.setTitleColor(UIColor(named: "inactiveText"), for: .normal)
        } else {
            self.buttonCC.setTitleColor(.black, for: .normal)
        }
        //self.buttonCC.setTitleColor(UIColor(named: "inactiveText"), for: .normal)
        lblCC.isHidden = true
    }
    
    
    @IBAction func btnChangePasswordAction(_ sender: Any) {
        let vc = self.storyboard?.instantiateViewController(withIdentifier: "ChangePasswordViewController") as! ChangePasswordViewController
        
        self.navigationController?.pushViewController(vc, animated: true)
    }
    
    @IBAction func btnCameraAction(_ sender: Any) {
        
    }
    
    @IBAction func btnSaveChanges(_ sender: Any) {
        if txtEmail.text!.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
            createalert(title: "Alert", message: "Email Name should not be empty", vc: self)
        }
        else if isValidEmail(testStr: txtEmail.text!) == false {
            createalert(title: "Alert", message: "Please enter valid email id ", vc: self)
        }
        else  if txtFirstname.text!.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
            createalert(title: "Alert", message: "First Name should not be empty", vc: self)
        }
        else  if txtLastName.text!.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
            createalert(title: "Alert", message: "Last Name should not be empty", vc: self)
        }
        else  if txtMobile.text!.trimmingCharacters(in: .whitespacesAndNewlines).count < 7 {
            createalert(title: "Alert", message: "Mobile Number should not be empty", vc: self)
        }
        else if buttonCC.currentTitle == "CC" {
            createalert(title: "Alert", message: "Country Code should not be empty", vc: self)
        }
        else {
            ApiCallToUpdateProfile()
        }
    }
    
    @IBAction func btnGenderDropDown(_ sender: Any) {
        setUpGenderXibFunc()
    }
    
    //    MARK:- Gender Xib
    func setUpGenderXibFunc () {
        requestViewGlobal1(vc: self)
        
        userTypeViewXib1.btnMaleFull.addTarget(self, action: #selector(btnMaleClick), for: .touchUpInside)
        userTypeViewXib1.btnMaleFull.tag = 0
        userTypeViewXib1.btnFemaleFull.addTarget(self, action: #selector(btnFeMaleClick), for: .touchUpInside)
        userTypeViewXib1.btnFemaleFull.tag = 1
        userTypeViewXib1.btnOtherFull.addTarget(self, action: #selector(btnOtherClick), for: .touchUpInside)
        userTypeViewXib1.btnOtherFull.tag = 2
        
        userTypeViewXib1.btnApply.addTarget(self, action: #selector(applyButtonClick), for: .touchUpInside)
        userTypeViewXib1.btnCancel.addTarget(self, action: #selector(cancelButtonClick), for: .touchUpInside)
        userTypeViewXib1.btnApply.layer.borderColor = UIColor.gray.cgColor
        userTypeViewXib1.btnApply.layer.borderWidth = 1
        userTypeViewXib1.btnCancel.layer.borderColor = UIColor.gray.cgColor
        userTypeViewXib1.btnCancel.layer.borderWidth = 1
        userTypeViewXib1.genderView.layer.cornerRadius = 5
        userTypeViewXib1.genderView.layer.shadowRadius = 1
        userTypeViewXib1.genderView.layer.shadowColor = UIColor.gray.cgColor
        userTypeViewXib1.genderView.layer.shadowOpacity = 0.4
        userTypeViewXib1.genderView.layer.shadowOffset = CGSize(width: -1, height: 4)
    }
    
    @objc func applyButtonClick(sender: UIButton!) {
        userTypeViewXib1.removeFromSuperview()
        self.txtGender.text = selectedGender
    }
    
    @objc func cancelButtonClick(sender: UIButton!) {
        UIView.animate(withDuration: 0.5, animations: {
            userTypeViewXib1.alpha = 0
        }) { (finished) in
            userTypeViewXib1.removeFromSuperview()
        }
    }
    @objc func btnMaleClick(sender: UIButton!) {
        if sender.tag == 0 {
            AllUnselected()
            MaleSelected()
            
        }
    }
    @objc func btnFeMaleClick(sender: UIButton!) {
        if sender.tag == 1 {
            AllUnselected()
            FemaleSelected()
        }
    }
    
    @objc func btnOtherClick(sender: UIButton!) {
        if sender.tag == 2 {
            AllUnselected()
            OtherSelected()
        }
    }
    func MaleSelected() {
        userTypeViewXib1.btnMale.setImage(UIImage(named: "radio_select"), for: .normal)
        self.maleSelect = true
        self.selectedGender = "male"
    }
    func FemaleSelected() {
        userTypeViewXib1.btnFemale.setImage(UIImage(named: "radio_select"), for: .normal)
        self.maleSelect = true
        self.selectedGender = "female"
    }
    func OtherSelected() {
        userTypeViewXib1.btnOther.setImage(UIImage(named: "radio_select"), for: .normal)
        self.otherSelect = true
        self.selectedGender = "other"
    }
    func AllUnselected() {
        userTypeViewXib1.btnMale.setImage(UIImage(named: "radio_unselect"), for: .normal)
        userTypeViewXib1.btnFemale.setImage(UIImage(named: "radio_unselect"), for: .normal)
        userTypeViewXib1.btnOther.setImage(UIImage(named: "radio_unselect"), for: .normal)
        
        self.maleSelect = false
        self.femaleSelect = false
        self.otherSelect = false
        
        self.selectedGender = " "
    }
    //MARK:- Api Calling
    func ApiCallTogetUserDetails() {
        getMethodWithAuthorizationReturnJson(apiName: "my-profile/", vc: self) { (response : JSON) in
            print(response)
            if response["status"].stringValue == "200" {
                let data = response["data"].dictionaryValue
                
                if  data["first_name"]?.stringValue != nil {
                    self.txtFirstname.text = data["first_name"]?.stringValue
                    self.firstNametxtTempActive()
                }
                if data["email"]?.stringValue != nil {
                    self.txtEmail.text = data["email"]?.stringValue
                    self.emailtxtTempActive()
                }
                if data["last_name"]?.stringValue != nil {
                    self.txtLastName.text = data["last_name"]?.stringValue
                    self.lastNametxtTempActive()
                }
                
                self.imgImage.image = UIImage(named: "temp_profile")
                if data["phone"]?.stringValue.isEmpty != true {
                    
                    self.mobiletxtTempActive()
                    let mobileNo = data["phone"]!.stringValue
                    print(mobileNo)
                    //   if mobileNo.count == 12 {
                    
                    self.txtMobile.text = String((data["phone"]?.stringValue)?.dropFirst(5) ?? "0")
                    let Code = "\(String(Array(mobileNo)[3]))\(String(Array(mobileNo)[4]))"
                    print(Code)
                    if self.ccCode.contains(Code) {
                        self.buttonCC.setTitle(Code, for: .normal)
                        self.buttonCC.setTitleColor(.black, for: .normal)
                    }
                }
                
                if data["gender"]?.stringValue != nil {
                    self.txtGender.text = data["gender"]?.stringValue
                    self.gendertxtTempActive()
                }
                else {
                    self.txtGender.text = ""
                }
            }
            self.imgImage.layer.cornerRadius = self.imgImage.frame.height/2
        }
    }
    
    func ApiCallToUpdateProfile () {
        let mobileNo = "971\(buttonCC.currentTitle!)\(txtMobile.text!)"
        var params = [String:Any]()
        params["first_name"] = self.txtFirstname.text
        params["last_name"] = self.txtLastName.text
        params["email"] = self.txtEmail.text
        params["phone"] = mobileNo
        params["gender"] = self.txtGender.text
        params["location"] = self.txtAddress.text
        params["carrier_code"] = Int(buttonCC.currentTitle!.trimmingCharacters(in: .whitespacesAndNewlines)) ?? 00
        print(params)
        //        putMethodReturnJson
        putMethodReturnJson(apiName: "my-profile/", params: params , vc : self) { (response : JSON) in
            //        requestWithPut(methodName: "my-profile/", parameter: params) { (response : JSON) in
            print(response)
            if response["status"].intValue == 200 {
                let msg = response["message"].stringValue
                self.showAlertOnProfileUpdate(message: msg)
            }
            else {
                createalert(title: "Alert", message: response["message"].stringValue, vc: self)
            }
        }
    }
    
    //    MARK:- Alert
    func showAlertOnProfileUpdate(message: String)
    {
        let alert = UIAlertController(title: "Success", message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .default, handler: { (_) in
            self.navigationController?.popViewController(animated: true)
        }))
        self.present(alert, animated: true, completion: nil)
    }
}
extension UpdateProfileViewController : UITextFieldDelegate {
    func textFieldDidBeginEditing(_ textField: UITextField) {
        if textField == txtFirstname {
            allInActive1()
            firstNametxtActive()
        }
        else if textField == txtLastName {
            allInActive1()
            lastNametxtActive()
        }
        else if textField == txtEmail {
            allInActive1()
            emailtxtActive()
        }
        else if textField == txtMobile {
            allInActive1()
            mobiletxtActive()
        }
        else if textField == txtGender {
            allInActive1()
            gendertxtActive()
        }
        else {
            allInActive1()
            addresstxtActive()
        }
    }
    
    //TextField Validation
    func textField(_ textField: UITextField, shouldChangeCharactersIn range: NSRange, replacementString string: String) -> Bool  {
        if(textField == txtFirstname)  {
            if string == " " {
                if range.location == 0 {
                    return false
                }
                return false
            }
            
            return true
        }
        else if(textField == txtLastName)  {
            if string == " " {
                if range.location == 0 {
                    return false
                }
                return false
            }
            
            return true
        }
        else if(textField == txtEmail) {
            if string == " " {
                if range.location == 0 {
                    return false
                }
                return false
            }
            
            return true
        }
        else if(textField == txtAddress) {
            if range.location == 0 && string == " " {
                return false
            }
            return true
        }
        else if let text:NSString = txtMobile.text as NSString? {
            let txtAfterUpdate = text.replacingCharacters(in: range, with: string)
            if txtAfterUpdate.count <= 7 {
                return true
            }
        }
            
        else {
            return true
        }
        return true
    }
}
// MARK:- CCTable data source and Delegate
extension UpdateProfileViewController : UITableViewDataSource, UITableViewDelegate {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return ccCode.count
    }
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = mobileCCTable.dequeueReusableCell(withIdentifier: "MobileCCTableViewCell") as! MobileCCTableViewCell
        cell.ccLabel.text = ccCode[indexPath.row]
        cell.selectionStyle = .none
        return cell
    }
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        self.buttonCC.setTitle(ccCode[indexPath.row], for: .normal)
        self.buttonCC.setTitleColor(.black, for: .normal)
        ccBackgroundView.alpha = 0
        ccTableView.alpha = 0
    }
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 50
    }
    
}
