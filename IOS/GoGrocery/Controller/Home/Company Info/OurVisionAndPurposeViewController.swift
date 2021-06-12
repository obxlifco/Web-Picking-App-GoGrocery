//
//  OurVisionAndPurposeViewController.swift
//  GoGrocery
//
//  Created by NAV63 on 30/03/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
import SwiftyJSON
class OurVisionAndPurposeViewController: UIViewController {
 @IBOutlet weak var lblAboutUs: UILabel!
      @IBOutlet weak var navigationView: UIView!
        var aboutUsArr = [JSON]()
    override func viewDidLoad() {
        super.viewDidLoad()
        ApiCallToDisplayData()
     
        self.navigationView.addShadow1()
        // Do any additional setup after loading the view.
    }
    
    @IBAction func btnBackAction(_ sender: Any) {
             self.navigationController?.popViewController(animated: true)
      }
        //    MARK:- Api Calling
        func ApiCallToDisplayData() {
            var params = [String:Any]()
            params["url"] = "ourvision-purpose"
            params["template_id"] = "1"
            params["company_website_id"] = "1"
            print(params)
            postMethodQuery1(apiName: "https://www.gogrocery.ae/api/front/v1/page_url_to_id/", params: params, vc: self) { (response : JSON) in
                print(response)
                self.aboutUsArr = response["cms_widgets"].arrayValue
                let aboutUsString = self.aboutUsArr[0]["property_value"].stringValue
                print(aboutUsString)
                let dict = self.convertToDictionary(text: aboutUsString)
                print(dict!)
                let insertArray = dict!["insertables"] as! NSArray
                print(insertArray)
                let insetDict = insertArray[0] as! NSDictionary
                print(insetDict)
                let propertyArary = insetDict["properties"] as! NSArray
                let propertyDict = propertyArary[0] as! NSDictionary
                let valueString = propertyDict["value"] as! String
             self.lblAboutUs.attributedText = valueString.htmlToAttributedString
        }
    }
        func convertToDictionary(text: String) -> [String: Any]? {
            if let data = text.data(using: .utf8) {
                do {
                    return try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any]
                } catch {
                    print(error.localizedDescription)
                }
            }
            return nil
        }

    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
