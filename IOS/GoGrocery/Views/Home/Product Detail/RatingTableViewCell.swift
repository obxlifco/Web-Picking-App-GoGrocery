//
//  RatingTableViewCell.swift
//  GoGrocery
//
//  Created by BMS-09-M on 17/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
import Cosmos
import GTProgressBar

class RatingTableViewCell: UITableViewCell {
    @IBOutlet weak var btnRate: UIButton!
    @IBOutlet weak var lblAvgRate: UILabel!
    @IBOutlet weak var lblOneRate: UILabel!
    @IBOutlet weak var lblTwoRate: UILabel!
    @IBOutlet weak var lblThreeRate: UILabel!
    @IBOutlet weak var lblFourRate: UILabel!
    @IBOutlet weak var lblFiveRate: UILabel!
    @IBOutlet weak var avgRatingView: CosmosView!
    @IBOutlet weak var star5ProgrressBar: GTProgressBar!
    @IBOutlet weak var star4ProgressBar: GTProgressBar!
    
    @IBOutlet weak var star3ProgressBar: GTProgressBar!
    
    @IBOutlet weak var star2ProgressBar: GTProgressBar!
    
    @IBOutlet weak var star1Progressbar: GTProgressBar!
    
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
