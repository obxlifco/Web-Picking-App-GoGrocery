//
//  MainMenuTableViewCell.swift
//  GoGrocery
//
//  Created by BMS-09-M on 26/12/19.
//  Copyright © 2019 BMS-09-M. All rights reserved.
//

import UIKit

class MainMenuTableViewCell: UITableViewCell {

    @IBOutlet weak var imgMenu: UIImageView!
    @IBOutlet weak var lblMainMenuName: UILabel!
     @IBOutlet weak var btnNext: UIButton!
    @IBOutlet weak var cellView: UIView!
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
