class Config:
    base_dir = './'
    dest_dir = 'output'
    ## serch and ingest
    api_key = ''
    ## videos origin
    orig_base = 'channel' # ['channel', 'playlist']
    ## Channels and Playlists files
    channels_file = './input/channels_id.txt'
    playlists_file = './input/playlists_id.txt'

    ignored_youtube_videos = ''
    downloaded_youtube_videos = 'downloaded_youtube_videos.txt'
    # logs
    logs_dir = 'logs'
    youtube_videos_error = 'error_youtube_videos.txt'
    log_file = 'errors.log'
    #channel_id  = 'UCEWHPFNilsT0IfQfutVzsag'
    output_search_file = 'youtube_videos.txt'
    # text_normalization
    min_words = 15
    max_words = 30
    # split_audio
    wavs_dir = 'wavs'
    metadata_subtitles_file = 'subtitles.csv'
    # convertion to transcript format
    tmp_wavs_dir = 'wavs_tmp'
    # transcribe
    transcription_file = 'transcript.csv'
    #output_converted_wavs_path = '00_16k'
    # validation
    validation_file = 'validation.csv'
    # selection
    minimal_levenshtein_distance = 0.9
    # downsampling
    sampling_rate = 22050
    # result
    result_file = 'metadata.csv'