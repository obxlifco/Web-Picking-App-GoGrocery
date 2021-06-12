//
//  ProfleImageTableViewCell.swift
//  GoGrocery
//
//  Created by Shanu on 30/12/19.
//  Copyright © 2019 BMS-09-M. All rights reserved.
//

import UIKit

class ProfleImageTableViewCell: UITableViewCell {
    @IBOutlet weak var imgProfile: UIImageView!
    @IBOutlet weak var lblName: UILabel!
    @IBOutlet weak var lblEmail: UILabel!
    @IBOutlet weak var btnEdit: UIButton!
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
