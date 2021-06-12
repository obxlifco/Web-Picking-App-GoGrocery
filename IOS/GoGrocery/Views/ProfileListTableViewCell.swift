//
//  ProfileListTableViewCell.swift
//  GoGrocery
//
//  Created by Shanu on 30/12/19.
//  Copyright © 2019 BMS-09-M. All rights reserved.
//

import UIKit

class ProfileListTableViewCell: UITableViewCell {
    @IBOutlet weak var imgTitle: UIImageView!
    @IBOutlet weak var lblTitleName: UILabel!
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
