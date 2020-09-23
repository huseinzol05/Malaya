from malaya.function import check_file, load_graph, generate_session
from malaya.text.bpe import SentencePieceEncoder, YTTMEncoder, load_yttm
from malaya.text.t2t import text_encoder


def load_lm(path, s3_path, model, model_class, **kwargs):
    check_file(path[model], s3_path[model], **kwargs)
    g = load_graph(path[model]['model'], **kwargs)
    X = g.get_tensor_by_name('import/Placeholder:0')
    top_p = g.get_tensor_by_name('import/Placeholder_1:0')
    greedy = g.get_tensor_by_name('import/greedy:0')
    beam = g.get_tensor_by_name('import/beam:0')
    nucleus = g.get_tensor_by_name('import/nucleus:0')

    tokenizer = SentencePieceEncoder(path[model]['tokenizer'])


def load(path, s3_path, model, encoder, model_class, **kwargs):
    check_file(path[model], s3_path[model], **kwargs)
    g = load_graph(path[model]['model'], **kwargs)

    if encoder == 'subword':
        encoder = text_encoder.SubwordTextEncoder(path[model]['vocab'])

    if encoder == 'yttm':
        bpe, subword_mode = load_yttm(path[model]['bpe'])
        encoder = YTTMEncoder(bpe, subword_mode)

    return model_class(
        g.get_tensor_by_name('import/Placeholder:0'),
        g.get_tensor_by_name('import/greedy:0'),
        g.get_tensor_by_name('import/beam:0'),
        generate_session(graph = g, **kwargs),
        encoder,
    )
