//
//  SlideTableViewCell.swift
//  GoGrocery
//
//  Created by BMS-09-M on 03/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
import SwiftyJSON
import ImageSlideshow
class SlideTableViewCell: UITableViewCell {
    
    @IBOutlet var slideshow: ImageSlideshow!
    var cellCaraouselArray = [JSON]()
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }
}
