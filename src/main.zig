const std = @import("std");

const converter = @import("converter");

const zglfw = @import("zglfw");
const zgpu = @import("zgpu");
const zgui = @import("zgui");

const ConverterErrors = error{
    WeirdGameDir,
};

const Settings = struct {
    input_folder_path: []const u8 = "",
    output_folder_path: []const u8 = "",
    game_executable_path: []const u8 = "",
};

pub fn main() !void {
    zglfw.init() catch {
        std.log.err("Failed to initialize GLFW library.", .{});
        return;
    };
    defer zglfw.terminate();

    const window = zglfw.Window.create(1600, 300, "Legacy Mod Converter v1.0 for CCCP v6.0.0", null) catch {
        std.log.err("Failed to create window.", .{});
        return;
    };
    defer window.destroy();
    // window.setSizeLimits(600, 400, -1, -1);

    var gpa_state = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa_state.deinit();
    const gpa = gpa_state.allocator();

    const gctx = try zgpu.GraphicsContext.create(gpa, window, .{});
    defer gctx.destroy(gpa);

    zgui.init(gpa);
    defer zgui.deinit();

    // _ = zgui.io.addFontFromFile("content/Roboto-Medium.ttf", 26.0);
    // _ = zgui.io.addFontFromFile("content/FiraCode-Medium.ttf", 26.0);
    _ = zgui.io.addFontFromFile("content/ProggyClean.ttf", 26.0);

    zgui.backend.init(
        window,
        gctx.device,
        @intFromEnum(zgpu.GraphicsContext.swapchain_format),
    );
    defer zgui.backend.deinit();

    const settings_text = std.fs.cwd().readFileAlloc(gpa, "settings.json", 1337) catch |err| switch (err) {
        error.FileNotFound => try gpa.dupe(u8, "{}"),
        else => return err,
    };
    defer gpa.free(settings_text);

    const settings_parsed = try std.json.parseFromSlice(Settings, gpa, settings_text, .{});
    defer settings_parsed.deinit();
    var settings = settings_parsed.value;

    var input_folder_path_mut: [std.fs.MAX_PATH_BYTES + 1:0]u8 = undefined;
    @memcpy(input_folder_path_mut[0..settings.input_folder_path.len], settings.input_folder_path);
    input_folder_path_mut[settings.input_folder_path.len] = 0;

    var output_folder_path_mut: [std.fs.MAX_PATH_BYTES + 1:0]u8 = undefined;
    @memcpy(output_folder_path_mut[0..settings.output_folder_path.len], settings.output_folder_path);
    output_folder_path_mut[settings.output_folder_path.len] = 0;

    var game_executable_path_mut: [std.fs.MAX_PATH_BYTES + 1:0]u8 = undefined;
    @memcpy(game_executable_path_mut[0..settings.game_executable_path.len], settings.game_executable_path);
    game_executable_path_mut[settings.game_executable_path.len] = 0;

    while (!window.shouldClose()) {
        zglfw.pollEvents();

        zgui.backend.newFrame(
            gctx.swapchain_descriptor.width,
            gctx.swapchain_descriptor.height,
        );

        // Set the starting window position and size to custom values
        zgui.setNextWindowPos(.{ .x = 0.0, .y = 0.0, .cond = .always });
        zgui.setNextWindowSize(.{ .w = -1.0, .h = -1.0, .cond = .always });
        // zgui.setNextWindowSize(.{ .w = 420, .h = 300, .cond = .always });

        if (zgui.begin("invisible_title", .{ .flags = .{ .no_title_bar = true, .no_resize = true, .no_background = true } })) {
            const padding = 15;
            const min_width = 855;

            zgui.setNextItemWidth(@max(zgui.calcTextSize(settings.input_folder_path, .{})[0] + padding, min_width));
            if (zgui.inputTextWithHint("Input/ folder path", .{ .hint = "Copy-paste a path from File Explorer here", .buf = &input_folder_path_mut })) {
                settings.input_folder_path = std.mem.span(@as([*:0]u8, &input_folder_path_mut));
                try writeSettings(settings);
            }

            zgui.setNextItemWidth(@max(zgui.calcTextSize(settings.output_folder_path, .{})[0] + padding, min_width));
            if (zgui.inputTextWithHint("Mods/ folder path", .{ .hint = "Copy-paste a path from File Explorer here", .buf = &output_folder_path_mut })) {
                settings.output_folder_path = std.mem.span(@as([*:0]u8, &output_folder_path_mut));
                try writeSettings(settings);
            }

            if (zgui.button("Convert", .{ .w = 200.0 })) {
                std.debug.print("Converting...\n", .{});

                var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
                defer arena.deinit();
                var allocator = arena.allocator();

                var diagnostics: converter.Diagnostics = .{};
                converter.convert(
                    settings.input_folder_path,
                    settings.output_folder_path,
                    allocator,
                    &diagnostics,
                ) catch |err| switch (err) {
                    error.UnexpectedToken => {
                        const token = diagnostics.token orelse "null";
                        const file_path = diagnostics.file_path orelse "null";
                        const line = diagnostics.line orelse -1;
                        const column = diagnostics.column orelse -1;

                        std.debug.print("Error: Unexpected '{s}' at {s}:{}:{}\n", .{
                            token,
                            file_path,
                            line,
                            column,
                        });

                        return err;
                    },
                    error.TooManyTabs => {
                        const file_path = diagnostics.file_path orelse "null";
                        const line = diagnostics.line orelse -1;
                        const column = diagnostics.column orelse -1;

                        std.debug.print("Error: Too many tabs at {s}:{}:{}\n", .{
                            file_path,
                            line,
                            column,
                        });

                        return err;
                    },
                    else => |e| return e,
                };

                try converter.beautifyLua(settings.output_folder_path, allocator);

                // TODO: Run .convert() in a separate thread, letting it update a passed Progress struct so we can update a progress bar here?
                // TODO: Check if std/Progress.zig is of use: https://ziglang.org/documentation/master/std/src/std/Progress.zig.html
                // TODO: Look at this example of multithreading in Zig: https://gist.github.com/cabarger/d3879745b8477670070f826cad2f027d
                // var progress: f32 = 0.0;
                // _ = progress;
                // zgui.pushStyleColor4f(.{ .idx = .plot_histogram, .c = .{ 0.1 + 0.5 * (1 - progress), 0.2 + 0.7 * progress, 0.3, 1.0 } });
                // zgui.progressBar(.{ .fraction = progress, .overlay = "" });
                // zgui.popStyleColor(.{});
                // progress += 0.01;
                // if (progress > 2.0) progress = 0.0;

                std.debug.print("Done converting!\n", .{});
            }

            zgui.setNextItemWidth(@max(zgui.calcTextSize(settings.game_executable_path, .{})[0] + padding, min_width));
            if (zgui.inputTextWithHint("Game .exe path", .{ .hint = "Copy-paste a path from File Explorer here", .buf = &game_executable_path_mut })) {
                settings.game_executable_path = std.mem.span(@as([*:0]u8, &game_executable_path_mut));
                try writeSettings(settings);
            }

            if (zgui.button("Launch", .{ .w = 200.0 })) {
                // TODO: Handle settings.game_executable_path not being set yet
                try std.os.chdir(std.fs.path.dirname(settings.game_executable_path) orelse return ConverterErrors.WeirdGameDir);
                var argv = [_][]const u8{settings.game_executable_path};
                const result = try std.ChildProcess.exec(.{ .argv = &argv, .allocator = gpa });
                _ = result;
            }
            if (zgui.button("Zip", .{ .w = 200.0 })) {
                var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
                defer arena.deinit();
                var allocator = arena.allocator();

                try converter.zipMods(settings.input_folder_path, settings.output_folder_path, allocator);

                std.debug.print("Done zipping!\n", .{});
            }
        }
        zgui.end();

        const swapchain_texv = gctx.swapchain.getCurrentTextureView();
        defer swapchain_texv.release();

        const commands = commands: {
            const encoder = gctx.device.createCommandEncoder(null);
            defer encoder.release();

            // GUI pass
            {
                const pass = zgpu.beginRenderPassSimple(encoder, .load, swapchain_texv, null, null, null);
                defer zgpu.endReleasePass(pass);
                zgui.backend.draw(pass);
            }

            break :commands encoder.finish(null);
        };
        defer commands.release();

        gctx.submit(&.{commands});
        _ = gctx.present();
    }
}

fn writeSettings(settings: Settings) !void {
    const output_file = try std.fs.cwd().createFile("settings.json", .{});
    defer output_file.close();

    var buffered = std.io.bufferedWriter(output_file.writer());
    const buffered_writer = buffered.writer();
    try std.json.stringify(settings, .{}, buffered_writer);
    try buffered.flush();
}
