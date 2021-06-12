//
//  ProductNameTableViewCell.swift
//  GoGrocery
//
//  Created by BMS-09-M on 17/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class ProductNameTableViewCell: UITableViewCell {
@IBOutlet weak var lblProductName: UILabel!
    @IBOutlet weak var lblBrandName: UILabel!
     @IBOutlet weak var lblCat: UILabel!
      @IBOutlet weak var btnCat: UIButton!
      @IBOutlet weak var lblSku: UILabel!
    
      @IBOutlet weak var lblProductNameHeight: NSLayoutConstraint!
     @IBOutlet weak var lblBrandNameHeight: NSLayoutConstraint!
     @IBOutlet weak var lblCatHeight: NSLayoutConstraint!
     @IBOutlet weak var btnCatHeight: NSLayoutConstraint!
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
