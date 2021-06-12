
import UIKit
import SwiftyJSON
class ResetPasswordViewController: UIViewController {

    @IBOutlet weak var navigationView: UIView!
    @IBOutlet weak var newPasswordTxt: UITextField!
    @IBOutlet weak var newPasswordLbl: UILabel!
    @IBOutlet weak var confirmPassTxt: UITextField!
    @IBOutlet weak var confirmPassLbl: UILabel!
    @IBOutlet weak var updateBtn: UIButton!
    @IBOutlet weak var newPassImage: UIImageView!
    @IBOutlet weak var confirmPassImage: UIImageView!
    var isNewPassShow = false
    var isConfirmPassShow = false
    var resetTokenInReset = String()
    override func viewDidLoad() {
        super.viewDidLoad()

        
        allInActive1()
        self.navigationView.addShadow1()
        newPasswordTxt.delegate = self
        confirmPassTxt.delegate = self
        newPasswordTxt.layer.cornerRadius = 5
        confirmPassTxt.layer.cornerRadius = 5
        
        newPasswordTxt.setLeftPaddingPoints(10)
        confirmPassTxt.setLeftPaddingPoints(10)
        
        updateBtn.layer.cornerRadius = 6
        updateBtn.clipsToBounds = true
        updateBtn.layer.borderWidth = 1
        updateBtn.layer.borderColor = UIColor.red.cgColor
        
        // Do any additional setup after loading the view.
    }
    override func viewWillAppear(_ animated: Bool) {
        print(resetTokenInReset)
        self.navigationController?.isNavigationBarHidden = true
    }
    
     //    MARK:- Active
     func newPasswordtxtActive() {
         self.newPasswordTxt.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
         self.newPasswordTxt.layer.borderWidth = 2
         self.newPasswordLbl.isHidden = false
         self.newPasswordLbl.textColor = UIColor(named: "buttonBackgroundColor")
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
    
    func confirmPassInActive() {
        confirmPassTxt.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        confirmPassTxt.layer.borderWidth = 2
        self.confirmPassLbl.isHidden = true
    }
    
    func allInActive1() {
        newPasswordTxt.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        newPasswordTxt.layer.borderWidth = 2
        self.newPasswordLbl.isHidden = true
        
        confirmPassTxt.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        confirmPassTxt.layer.borderWidth = 2
        self.confirmPassLbl.isHidden = true
        
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
    
    @IBAction func updateBtnTapped(_ sender: Any) {

         if newPasswordTxt.text!.trimmingCharacters(in: .whitespaces).isEmpty {
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
        params["new_password"] = newPasswordTxt.text!
        params["confirm_password"] = confirmPassTxt.text!
        params["pin_code"] = resetTokenInReset
        print(params)
        
        postMethodQueryWithoutAuthorization(apiName: "confirm-password/", params: params, vc: self) { (response : JSON) in
            print(response)
            if response["status"].intValue == 1 {
            self.showAlertOnReset(message: response["message"].stringValue)
            }
            else {
                createalert(title: "Alert", message: response["message"].stringValue, vc: self)
            }
        }
        
    }
    
    //    MARK:- Alert
    func showAlertOnReset(message: String)
    {
        let alert = UIAlertController(title: "Success", message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .default, handler: { (_) in
//             let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
//            let vc = storyboard.instantiateViewController(withIdentifier: "MarkLocationViewController") as! MarkLocationViewController
//            self.navigationController?.pushViewController(vc, animated: true)
            
//            let testController = UIStoryboard(name: "Main", bundle: nil).instantiateViewController(withIdentifier: "MarkLocationViewController") as! MarkLocationViewController
//            let appDelegate = UIApplication.shared.delegate as! AppDelegate
//            appDelegate.window?.rootViewController = testController
            
//            let storyboard : UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
//            let vc : MarkLocationViewController = storyboard.instantiateViewController(withIdentifier: "MarkLocationViewController") as! MarkLocationViewController
//            let navigationController = UINavigationController(rootViewController: vc)
//            navigationController.modalPresentationStyle = UIModalPresentationStyle.fullScreen
//            self.present(navigationController, animated: true, completion: nil)
            
            
            
            let mainVC = UIStoryboard.init(name: "Main", bundle: nil).instantiateViewController(withIdentifier: "MarkLocationViewController") as! MarkLocationViewController
            let mainNav = UINavigationController.init(rootViewController: mainVC)
          //  mainNav.resetTokenInReset = resetToken
            appdelegate.window?.rootViewController = mainNav
            
        }))
        self.present(alert, animated: true, completion: nil)
    }
}
extension ResetPasswordViewController : UITextFieldDelegate {
    func textFieldDidBeginEditing(_ textField: UITextField) {
        if textField == newPasswordTxt {
            allInActive1()
            newPasswordtxtActive()
        }
        else if textField == confirmPassTxt {
            allInActive1()
            confirmPasstxtActive()
        }
        
    }
    
    //TextField Validation
        func textField(_ textField: UITextField, shouldChangeCharactersIn range: NSRange, replacementString string: String) -> Bool  {

             if(textField == newPasswordTxt)  {
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
