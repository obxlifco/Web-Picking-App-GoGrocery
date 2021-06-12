//
//  ReplaceTableViewCell.swift
//  GoGrocery
//
//  Created by NAV63 on 25/08/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class ReplaceTableViewCell: UITableViewCell {
    
    @IBOutlet weak var repOutOfStock: UILabel!
    @IBOutlet weak var repProductName: UILabel!
    @IBOutlet weak var repWeight: UILabel!
    @IBOutlet weak var repPrice: UILabel!
    @IBOutlet weak var repChooseReplacement: UILabel!
    @IBOutlet weak var repImage: UIImageView!
    @IBOutlet weak var repProductView: UIView!
    @IBOutlet weak var repoCollectionView: UICollectionView!
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
