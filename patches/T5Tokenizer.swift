//
//  T5Tokenizer.swift
//  (Disabled – not used in SemanticCompression)
//

import Foundation
import Hub
import Tokenizers

public extension Config {
    /// Disabled override – not required for our use case.
    init(fileURL: URL) throws {
        throw Hub.HubClientError.parse
    }
}
