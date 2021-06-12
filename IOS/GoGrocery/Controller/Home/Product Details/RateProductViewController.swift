
import UIKit
import Cosmos
import SwiftyJSON
class RateProductViewController: UIViewController {
    @IBOutlet weak var ratingView: CosmosView!
    @IBOutlet weak var ratingLabel: UILabel!
    @IBOutlet weak var reviewTitleTextField: UITextField!
    @IBOutlet weak var reviewTitleLabel: UILabel!
    @IBOutlet weak var reviewDescriptionTextField1: UITextField!
    @IBOutlet weak var reviewDescriptionTextField: UITextView!
    @IBOutlet weak var reviewDescriptionLabel: UILabel!
    
    @IBOutlet weak var cancelBtn: UIButton!
    @IBOutlet weak var submitButton: UIButton!
    var totalRating:Double = 0
    var productId = 0
    override func viewDidLoad() {
        super.viewDidLoad()

        allInActive1()
        reviewTitleTextField.delegate = self
        reviewDescriptionTextField.delegate = self
        
        reviewTitleTextField.layer.cornerRadius = 5
        reviewDescriptionTextField.layer.cornerRadius = 5
        reviewDescriptionTextField.text = "Enter Review Description"
        reviewDescriptionTextField.textColor = UIColor.lightGray
        reviewTitleTextField.setLeftPaddingPoints(10)
        //reviewDescriptionTextField.setLeftPaddingPoints(10)
        
        submitButton.layer.cornerRadius = 6
        submitButton.clipsToBounds = true
        submitButton.layer.borderWidth = 1
        submitButton.layer.borderColor = UIColor.red.cgColor
        
        cancelBtn.layer.cornerRadius = 6
        cancelBtn.clipsToBounds = true
        cancelBtn.layer.borderWidth = 1
        cancelBtn.layer.borderColor = UIColor.red.cgColor
        // Do any additional setup after loading the view.
        ratingView.didTouchCosmos = { rating in
            if rating == 5 {
                self.ratingLabel.text = "Very Good"
                self.ratingLabel.textColor = #colorLiteral(red: 0.0431372549, green: 0.5803921569, blue: 0.2666666667, alpha: 1)
            } else if rating == 4 {
                self.ratingLabel.text = "Good"
                self.ratingLabel.textColor = #colorLiteral(red: 0.0431372549, green: 0.5803921569, blue: 0.2666666667, alpha: 1)
            } else if rating == 3 {
                self.ratingLabel.text = "Good"
                self.ratingLabel.textColor = #colorLiteral(red: 0.0431372549, green: 0.5803921569, blue: 0.2666666667, alpha: 1)
            } else if rating == 2 {
                self.ratingLabel.text = "Average"
                self.ratingLabel.textColor = #colorLiteral(red: 1, green: 0.6235294118, blue: 0, alpha: 1)
            } else if rating == 1 {
                self.ratingLabel.text = "Worst"
                self.ratingLabel.textColor = #colorLiteral(red: 1, green: 0.3803921569, blue: 0.3803921569, alpha: 1)

            }
        }
        ratingView.didFinishTouchingCosmos = { rating in
            self.totalRating = rating
        }
    }
    
    override func viewWillAppear(_ animated: Bool) {
        self.navigationController?.isNavigationBarHidden = true
    }
    
    func titleTxtActive() {
        self.reviewTitleTextField.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.reviewTitleTextField.layer.borderWidth = 2
        self.reviewTitleLabel.isHidden = false
        self.reviewTitleLabel.textColor = UIColor(named: "buttonBackgroundColor")
    }
    func descriptionTxtActive() {
        self.reviewDescriptionTextField.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
        self.reviewDescriptionTextField.layer.borderWidth = 2
        self.reviewDescriptionLabel.isHidden = false
        self.reviewDescriptionLabel.textColor = UIColor(named: "buttonBackgroundColor")
    }
    //    MARK:- Inactive
    func titleTxtInActive() {
        reviewTitleTextField.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        reviewTitleTextField.layer.borderWidth = 2
        self.reviewTitleLabel.isHidden = true
    }
    func descriptionTxtInActive() {
        reviewDescriptionTextField.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        reviewDescriptionTextField.layer.borderWidth = 2
        self.reviewDescriptionLabel.isHidden = true
    }
    func allInActive1() {
        reviewTitleTextField.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        reviewTitleTextField.layer.borderWidth = 2
        self.reviewTitleLabel.isHidden = true
        
        reviewDescriptionTextField.layer.borderColor = UIColor(named: "inactiveText")?.cgColor
        reviewDescriptionTextField.layer.borderWidth = 2
        self.reviewDescriptionLabel.isHidden = true
    }
    
    @IBAction func backButtonTapped(_ sender: Any) {
        self.navigationController?.popViewController(animated: true)
    }
    @IBAction func submitButtonTapped(_ sender: Any) {
        if reviewTitleTextField.text!.trimmingCharacters(in: .whitespaces).isEmpty {
            createalert(title: "Alert", message: "Please enter title of review", vc: self)
        }
        else if reviewDescriptionTextField.text!.trimmingCharacters(in: .whitespaces).isEmpty {
            createalert(title: "Alert", message: "Please enter description of review", vc: self)
        }
        else if totalRating == 0 {
            createalert(title: "Alert", message: "Please give rating to product", vc: self)
        }
        else {
            apiCallToRateProduct()
        }
    }
    @IBAction func cancelButtonTapped(_ sender: Any) {
        self.navigationController?.popViewController(animated: true)
    }
    
    func apiCallToRateProduct() {
        var params = [String:Any]()
        params["product_id"] = productId
        params["review_title"] = reviewTitleTextField.text!
        params["review_message"] = reviewDescriptionTextField.text!
        params["review_star"] = Int(totalRating)
        // print(params)
        postMethodQuery2(apiName: "product-review/", params: params, vc: self) { (response : JSON) in
              print(response)
            if response["status"].intValue == 1 {
                let msg = response["msg"].stringValue
                createalert(title: "Alert", message: msg, vc: self)
                self.reviewTitleTextField.text = ""
                self.reviewDescriptionTextField.text = "Enter Review Description"
                self.reviewDescriptionTextField.textColor = UIColor.lightGray
            }
            else {
                let msg = response["msg"].stringValue
                createalert(title: "Alert", message: msg, vc: self)
                
            }
        }
    }
    

}
extension RateProductViewController : UITextFieldDelegate {
    func textFieldDidBeginEditing(_ textField: UITextField) {
        if textField == reviewTitleTextField {
            allInActive1()
            titleTxtActive()
        }
        
    }
    
}
extension RateProductViewController : UITextViewDelegate {
    func textViewDidBeginEditing(_ textView: UITextView) {
        if textView.textColor == UIColor.lightGray {
            textView.text = nil
            textView.textColor = UIColor.black
        }
        allInActive1()
        descriptionTxtActive()
    }
    func textViewDidEndEditing(_ textView: UITextView) {
        if textView.text.isEmpty {
            textView.text = "Enter Review Description"
            textView.textColor = UIColor.lightGray
        }
    }
}

