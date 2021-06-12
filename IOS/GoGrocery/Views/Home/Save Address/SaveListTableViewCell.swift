//
//  SaveListTableViewCell.swift
//  GoGrocery
//
//  Created by BMS-09-M on 29/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class SaveListTableViewCell: UITableViewCell {

      @IBOutlet var lblName: UILabel!
      @IBOutlet var lblArea: UILabel!
      @IBOutlet var lblCountry: UILabel!
      @IBOutlet var lblMobile: UILabel!
     @IBOutlet var lblDefault: UILabel!
      @IBOutlet var btneEditOrDelete: UIButton!
      @IBOutlet var btnAddressSelect: UIButton!
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
