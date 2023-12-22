from functools import wraps
import os
import pickle

# features:
# save format, interval (monthly, daily)


def load_file_handler(file_name, format):
    if format == "pickle":
        with open(file_name, "rb") as handler:
            obj = pickle.load(handler)

    print(f"Read from {file_name}")
    return obj


def save_file_handler(obj, file_name, format):
    if format == "pickle":
        with open(file_name, "wb") as pickle_handler:
            pickle.dump(obj, pickle_handler, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"Saved to {file_name}")


def full_file_name(location, func_name, format, *args, **kwargs):
    args_list = [str(arg) for arg in args]
    kwargs_list = [f"{key}_{val}" for key, val in kwargs.items()]
    file_name = f"{location}/{func_name}_{'_'.join(args_list + kwargs_list)}"
    format_mapping = {"pickle": "pkl"}
    return f"{file_name}.{format_mapping.get(format)}"


def local_saving(location: str = "temp", format: str = "pickle", force_reload=False):
    def inner_saving(func):
        @wraps(func)
        def saving_wrapper(*args, **kwargs):
            if not os.path.exists(location):
                os.makedirs(location)
            file_name = full_file_name(location, func.__name__, format, *args, **kwargs)
            if not force_reload and os.path.isfile(file_name):
                return load_file_handler(file_name, format)
            else:
                func_result = func(*args, **kwargs)
                save_file_handler(func_result, file_name, format)
                return func_result

        return saving_wrapper

    return inner_saving


