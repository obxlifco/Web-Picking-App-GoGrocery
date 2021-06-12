//
//  ProductPriceTableViewCell.swift
//  GoGrocery
//
//  Created by BMS-09-M on 17/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class ProductPriceTableViewCell: UITableViewCell {
    @IBOutlet weak var lblProductprice: UILabel!
     @IBOutlet weak var lblProductWeight: UILabel!
    @IBOutlet weak var lblProductDiscount: UILabel!
     @IBOutlet weak var lblStrikedPrice: UILabel!
     @IBOutlet weak var lblStrikedWidth: NSLayoutConstraint!
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
