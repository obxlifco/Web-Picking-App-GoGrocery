//
//  SaveTableViewCell.swift
//  GoGrocery
//
//  Created by Shanu on 19/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class SaveTableViewCell: UITableViewCell {
    @IBOutlet weak var btnEdit: UIButton!
    @IBOutlet weak var lblName: UILabel!
    @IBOutlet weak var lblDate: UILabel!
     @IBOutlet weak var lblItemCount: UILabel!
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
