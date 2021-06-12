//
//  ProductImageTableViewCell.swift
//  GoGrocery
//
//  Created by BMS-09-M on 17/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class ProductImageTableViewCell: UITableViewCell {
//@IBOutlet weak var imgProductImage: UIImageView!
    @IBOutlet weak var imgCollection: UICollectionView!
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
