//
//  FilterHeaderTableViewCell.swift
//  GoGrocery
//
//  Created by BMS-09-M on 14/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class FilterHeaderTableViewCell: UITableViewCell {

    @IBOutlet weak var btnHeader: UIButton!
    @IBOutlet weak var lblHeader: UILabel!
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }
    
}
