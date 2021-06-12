//
//  ReviewTableViewCell.swift
//  GoGrocery
//
//  Created by Nav121 on 18/02/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class ReviewTableViewCell: UITableViewCell {
    @IBOutlet weak var ratingCountView: UIView!
    
    @IBOutlet weak var ratingLbl: UILabel!
    
    @IBOutlet weak var reviewTitleLbl: UILabel!
    @IBOutlet weak var reviewDescriptionLable: UILabel!
    
    @IBOutlet weak var userInfoLbl: UILabel!
    
    @IBOutlet weak var seeAllView: UIView!
    
    @IBOutlet weak var viewAllBtn: UIButton!
    
    @IBOutlet weak var reviewView: CardView!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
