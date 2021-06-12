//
//  ViewAllReviewViewController.swift
//  GoGrocery
//
//  Created by Nav121 on 18/02/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
import SwiftyJSON

class ViewAllReviewViewController: UIViewController {

    @IBOutlet weak var tableView: UITableView!
    var allReviewData = [JSON]()
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }
    override func viewWillAppear(_ animated: Bool) {
        self.navigationController?.isNavigationBarHidden = true
    }
    @IBAction func backButtonTapped(_ sender: Any) {
        self.navigationController?.popViewController(animated: true)
    }
    

}

extension ViewAllReviewViewController : UITableViewDelegate , UITableViewDataSource {
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return allReviewData.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell5 = tableView.dequeueReusableCell(withIdentifier: "AllReviewTableViewCell") as! ReviewTableViewCell
       
        cell5.ratingCountView.layer.cornerRadius = cell5.ratingCountView.bounds.height / 2
        //cell5.reviewDescriptionLable.text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book"
        let reviewInfo = self.allReviewData[indexPath.row]
        if reviewInfo["rating"].intValue == 5 {
            cell5.ratingCountView.backgroundColor = #colorLiteral(red: 0.0431372549, green: 0.5803921569, blue: 0.2666666667, alpha: 1)
        } else if reviewInfo["rating"].intValue == 4 {
            cell5.ratingCountView.backgroundColor = #colorLiteral(red: 0.0431372549, green: 0.5803921569, blue: 0.2666666667, alpha: 1)
        } else if reviewInfo["rating"].intValue == 3 {
            cell5.ratingCountView.backgroundColor = #colorLiteral(red: 0.0431372549, green: 0.5803921569, blue: 0.2666666667, alpha: 1)
        } else if reviewInfo["rating"].intValue == 2 {
            cell5.ratingCountView.backgroundColor = #colorLiteral(red: 1, green: 0.6235294118, blue: 0, alpha: 1)
        } else if reviewInfo["rating"].intValue == 1 {
            cell5.ratingCountView.backgroundColor = #colorLiteral(red: 1, green: 0.3803921569, blue: 0.3803921569, alpha: 1)
        }
        cell5.ratingLbl.text = "\(reviewInfo["rating"].intValue)"
        cell5.reviewTitleLbl.text = reviewInfo["title"].stringValue
        cell5.reviewDescriptionLable.text = reviewInfo["review"].stringValue
        let dateFormatter = DateFormatter()
        let createdDate = dateFormatter.date(fromSwapiString: reviewInfo["created"].stringValue)
        
        dateFormatter.dateFormat = "dd MMM YYYY"

        let dateString = dateFormatter.string(from: createdDate!)
        cell5.userInfoLbl.text = "\(reviewInfo["user_name"].stringValue) , \(dateString)"
        return cell5
    }
    
    
    
    
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return UITableView.automaticDimension
    }
    
    func tableView(_ tableView: UITableView, estimatedHeightForRowAt indexPath: IndexPath) -> CGFloat
    {
     
     return 110
    }
    
}
